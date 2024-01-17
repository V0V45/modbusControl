import minimalmodbus

# Приветствие
print('Программа управления ПЧ MCI и FCI через Modbus RTU')

# Блок ввода исходных данных
# Порт, адрес, скорость
port = input('Порт (COM1, COM2, и т.д.): ')
slave_address = int(input('Локальный адрес устройства: '))
baud_rate = int(input('Скорость: '))

# Формат данных
byte_size = int(input('Формат данных; размер байта: (5, 6, 7, 8): '))
parity = input('Формат данных; четность (NONE, EVEN, ODD): ')
stop_bits = int(input('Формат данных; стоп-бит (1, 2): '))

# Задаем порт и адрес устройства
instrument = minimalmodbus.Instrument(port, slave_address)
# Задаем скорость
instrument.serial.baudrate = baud_rate
# Задаем формат данных; размер байта
instrument.serial.bytesize = byte_size
# Задаем формат данных; четность
if parity == 'NONE':
	instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
elif parity == 'EVEN':
	instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
elif parity == 'ODD':
	instrument.serial.parity = minimalmodbus.serial.PARITY_ODD
else:
	print('Четность была задана неверно; оставлено значение по умолчанию (NONE)')
# Задаем формат данных; стоп-бит
instrument.serial.stopbits = stop_bits

# Выводим итоговую информацию
print(f'''Порт: {instrument.serial.port},
Локальный адрес устройства: {instrument.address},
Скорость: {instrument.serial.baudrate}
Формат данных: {instrument.serial.bytesize} - {instrument.serial.parity} - {instrument.serial.stopbits}''')

# Проверка связи
print('Проверка связи: попытка считать напряжение на ЗПТ')
try:
    print(f'Связь установлена: напряжение на ЗПТ {instrument.read_register(36868, 1, functioncode=3)}')
except IOError:
    print('Ошибка связи! Не удалось считать напряжение на ЗПТ')
    sys.exit()

# Запуск работы программы
# Начальные значения
print('Управление запущено. Для выхода с программы введите значение регистра "99999"')
register = int(input('Введите регистр, к которому будем обращаться: '))

readorwrite = int(input('Введите функцию (6 - запись, 3 - чтение): '))
if readorwrite == 3:
	print('Считывание регистра.')
elif readorwrite == 6:
	register_value = float(input('Введите значение, которое будем записывать: '))
else:
	print('Значение функции задано неверно.')

while register != 99999:
	if readorwrite == 3:
		try:
			print(f'Значение регистра {register}: {instrument.read_register(register, 1, functioncode=readorwrite)}')
		except IOError:
			print(f'Ошибка чтения регистра.')
	elif readorwrite == 6:
		try:
			print(f'Попытка записи регистра {register}: ')
			instrument.write_register(register, register_value, 1, functioncode=readorwrite)
			print(f'Успешная запись регистра. Новое значение: {register_value}')
		except IOError:
			print(f'Ошибка записи регистра')
	else:
		print('Ошибка ввода. Начинаем сначала.')
	
	try:
		register = int(input('Введите регистр, к которому будем обращаться: '))
	except:
		print('Регистр введен неправильно.')

	readorwrite = int(input('Введите функцию (6 - запись, 3 - чтение): '))
	if readorwrite == 3:
		print('Считывание регистра.')
	elif readorwrite == 6:
		register_value = float(input('Введите значение, которое будем записывать: '))
	else:
		print('Значение функции задано неверно.')

# Баги: прога заканчивается не сразу