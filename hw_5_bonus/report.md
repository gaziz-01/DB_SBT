## 1) Реализованы процедуры добавления денег на баланс:
```lua
function add_funds(user_id, amount)
    local balance = box.space.balances:get(user_id)
    if balance then
        box.space.balances:update(user_id, {{'+', 2, amount}})
    else
        box.space.balances:insert({user_id, amount, 0})
    end
end
```
И изменение расхода денег в секунду
```lua
function set_expense_rate(user_id, rate)
    box.space.balances:update(user_id, {{'=', 3, rate}})
end
```
Для их проверки написаны тесты с использованием встроенного модуля tap в Tarantool.

## 2) Рассмотрен случай для клиентов с нулевым балансом

## 3) Использован шардинг с помощью vshard

![](/hw_5_bonus/1.png?raw=true)
![](/hw_5_bonus/2.png?raw=true)