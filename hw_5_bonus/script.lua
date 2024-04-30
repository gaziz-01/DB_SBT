local vshard = require('vshard')
local fiber = require('fiber')
local expirationd = require('expirationd')

box.cfg {
    listen = 3301, 
    wal_mode = 'write',
    log_level = 5
}

-- Настройка vshard
vshard_cfg = {
    sharding = {
        ['shard_uuid_1'] = {
            replicas = {
                ['replica_uuid_1'] = {
                    uri = 'localhost:3301',
                    name = 'replica_1',
                    zone = 1,
                    master = true  -- мастер-реплика
                }
            }
        }
    }
}
vshard.router.cfg(vshard_cfg)

-- Храненим балансы пользователей
box.once('init', function()
    local space = box.schema.space.create('balances', {if_not_exists = true})
    space:format({
        {name = 'user_id', type = 'string'},
        {name = 'balance', type = 'number'},
        {name = 'expense_rate', type = 'number'},  -- расход в секунду
    })
    space:create_index('primary', {parts = {'user_id'}, if_not_exists = true})
end)

-- Добавление денег на баланс
function add_funds(user_id, amount)
    local balance = box.space.balances:get(user_id)
    if balance then
        box.space.balances:update(user_id, {{'+', 2, amount}})
    else
        box.space.balances:insert({user_id, amount, 0})
    end
end

-- Изменение расхода денег в секунду
function set_expense_rate(user_id, rate)
    box.space.balances:update(user_id, {{'=', 3, rate}})
end

local http_client = require('http.client').new()

local function check_balance()
    for _, tuple in box.space.balances:pairs() do
        if tuple.balance <= 0 then
            http_client:get('http://example.com/api/notify?user_id=' .. tuple.user_id)
            box.space.balances:delete(tuple.user_id) 
        end
    end
end

-- Запуск задачи на периодическую проверку баланса
fiber.create(function()
    while true do
        check_balance()
        fiber.sleep(1)  -- проверка каждую секунду
    end
end)

-- Тесты
local tap = require('tap')
local test = tap.test('billing_tests')
test:plan(2)  

-- Добавление баланса
test:test("Add funds test", function(test)
    test:plan(1)
    add_funds('user1', 100)
    local user_balance = box.space.balances:get('user1')[2]
    test:is(user_balance, 100, "Balance should be correctly updated")
end)

-- Изменение расхода денег
test:test("Change expense rate test", function(test)
    test:plan(1)
    set_expense_rate('user1', 5)
    local user_expense_rate = box.space.balances:get('user1')[3]
    test:is(user_expense_rate, 5, "Expense rate should be correctly updated")
end)

test:check()
os.exit()