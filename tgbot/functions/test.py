from tgbot.database.DB import *

def declension_of_referral(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return 'реферал'
    elif n % 10 in [2, 3, 4] and n % 100 not in [12, 13, 14]:
        return 'реферала'
    else:
        return 'рефералов'



def top_10():
    data = Database().up_sub()
    sorted_data = sorted(data, key=lambda x: x[4], reverse=True)
    # Получение первых 10 элементов
    top_10 = sorted_data[:10]
    # Формирование строки из первых 10 элементов
    output_str = '\n'.join(f'╠ @{i[2]}: <code>{i[4]}</code> {declension_of_referral(int(i[4]))}\n╚<b>Дата регистрации:</b><code>{time.strftime("%d.%m.%y", time.localtime(int(i[3])))}</code>' for i in top_10)
    return output_str


print(top_10())