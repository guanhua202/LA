from time import sleep

requests = []

# -------------------------------------------UI--------------------------------------------
def menu_rendering():
	print("\n           📊 Анализатор логов\n")
	print('''1. Вывести всю активность\n2. Все запросы (Успешные/Перенаправления/Ошибки)\n3. Фильтрация по колонкам\n4. Записать лог файл\n0. Закрыть''')
	print("------------------------")

	global start_menu

	start_menu = int(input("Выберите пункт меню: "))

def render_table_of_ip():
	print('---------------------------------------------------------')
	print(f'''ID | IP           | METHOD | PATH      | STATUS''')
	print('---------------------------------------------------------')

# ----------------------------------------FUNCTIONS----------------------------------------

# --------------------------------------SMALL FUNCTIONS----------------------------------

def get_unique_ips():
	unique_ips = {data['ip'] for data in requests}

	return unique_ips

def check_void_logs():
	if requests == []:
		return False
	else:
		return True

def render_msg_void_logs():
	print('-----------------')
	print('Логи пустые.')
	print('-----------------')

def file_to_dict(file):
	request_id = 1

	for line in file.readlines():
		line = line.strip().split()

		if line == []:
			continue
		else:
			line = dict(ID=request_id, ip=line[0], method=line[1], path=line[2], status=int(line[3]))

			if line in requests:
				request_id += 1
				continue
			else:
				request_id += 1
				requests.append(line)
				print('Загрузка...')
				sleep(0.5)
		# ФОРМАТ ЗАПИСИ ЛОГОВ: IP | METHOD | PATH | STATUS

	sleep(0.5)
	print('----------------------------')
	print('Логи успешно добавлены. ✅')
	print('----------------------------')
	sleep(0.5)

def show_log_menu():
	
	def autoload_file():
		with open(input("Название файла для загрузки: ")) as file:
			file_to_dict(file)

	def write_log_entry():
		with open(input("Название нового/старого лог-файла: "), 'a') as file:
			file.write("\n" + input("\nЗаполните таблицу (IP | METHOD | PATH | STATUS): "))

			sleep(0.5)
			print('----------------------------')
			print(f"Данные успешно записаны в файл {file.name} ✅")
			print('----------------------------')
			sleep(0.5)

	print('\n------📝 Параметры записи логов-----------')
	print('1. Загрузить файл')
	print('2. Создание лог-файла (Не загрузка)')
	print('----------------------------')

	parametrs = {
			1 : autoload_file,
			2 : write_log_entry,
	}

	param = int(input("Выберите опцию: "))

	parametrs[param]() # Вызов
# -----------------------------------------------------------------------------------------

# -------------------------------------MAIN FUNCTIONS--------------------------------------

def get_ips_only():

	if check_void_logs():
		print('-----------------')
		print('ID | IP |')
		print('-----------------')
		
		request_id = 0

		for ip in get_unique_ips():
			request_id += 1
			print(f'{str(request_id).ljust(2)} | {ip}')
			sleep(0.5)
	else:
		render_msg_void_logs()

def show_all_logs():
	render_table_of_ip()

	if requests == []:
		print("Ничего не найдено.")
		sleep(0.5)
	else:
		for data in requests:
			print(f"{str(data['ID']).ljust(2)} | {data['ip'].ljust(12)} | {data['method'].ljust(6)} | {data['path'].ljust(9)} | {data['status']}")
			sleep(0.5)
	print('---------------------------------------------------------')
	sleep(1)
	input("Нажмите Enter, чтобы продолжить...")

def show_status_stats():
	succs_request = 0
	refer_request = 0
	err_request = 0

	for data in requests:
		if data['status'] // 100 == 2:
			succs_request += 1
		elif data['status'] // 100 == 3:
			refer_request += 1
		elif data['status'] // 100 == 4 or data['status'] // 100 == 5:
			err_request += 1

	sleep(1)
	print('------------------------')
	print(f'Успешных: {succs_request}, Перенаправлений: {refer_request}, Ошибок: {err_request}')
	print('------------------------')
	sleep(1)
	input("Нажмите Enter, чтобы продолжить...")

def get_one_ip_stats():

	if check_void_logs():
		get_ips_only()

		select_ip = int(input("Выберите IP адрес для фильтрации: "))
		request_id = 0
		found_ip = ""

		for ip in get_unique_ips():
			request_id += 1

			if select_ip == request_id:
				found_ip = ip
				break

		if found_ip == "":
			print("Ошибка! Выберите IP из списка.")
		else:
			render_table_of_ip()

			for data in requests:
				if data["ip"] == found_ip:
					print(f"{str(data['ID']).ljust(2)} | {data['ip'].ljust(12)} | {data['method'].ljust(6)} | {data['path'].ljust(9)} | {data['status']}")
					sleep(0.5)
		print('---------------------------------------------------------')
		input("Нажмите Enter, чтобы продолжить...")
	else:
		render_msg_void_logs()

def show_top_paths():
	if check_void_logs():

		paths = [data['path'] for data in requests]

		for i in range(0, len(paths) - 1):
			if paths.count(paths[i]) < paths.count(paths[i + 1]):
				paths[i], paths[i + 1] = paths[i + 1], paths[i]

		paths = sorted(set(paths))

		print('------------------------------')
		print('ID |   PATH   | TOTAL_REQUESTS')
		print('------------------------------')
		sleep(0.5)

		path_id = 0

		for path in paths:
			path_id += 1
			print(f"{str(path_id).ljust(2)} | {path.ljust(8)} | {[data['path'] for data in requests].count(path)}")
			sleep(0.5)
		print('-----------------')
		input("Нажмите Enter, чтобы продолжить...")
	else:
		render_msg_void_logs()

def filters_only_columns():
	print('\n---------📖 Фильтрация по колонкам---------')
	print('1. Все IP адреса (без повторений)')
	print('2. Активность конкретного IP (Фильтрация)')
	print('3. ТОП-страниц по запросам')
	print('------------------------')

	choice = int(input("Выберите опцию: "))

	filter_menu = {
		1 : get_ips_only,
		2 : get_one_ip_stats,
		3 : show_top_paths,
	}

	while choice not in filter_menu.keys():
		print('\nНет такого выбора в меню.\n')
		print('\n---------📖 Фильтрация по колонкам---------')
		print('1. Все IP адреса (без повторений)\n2. Активность конкретного IP (Фильтрация)\n3. ТОП-страниц по запросам')
		print('------------------------')

		choice = int(input("Выберите опцию: "))
	else:
		filter_menu[choice]()

# -------------------------------------------------------------------------------------------

# load_logs()
menu_rendering()

while start_menu != 0:

	menu_options = {
		1 : show_all_logs,
		2 : show_status_stats,
		3 : filters_only_columns,
		4 : show_log_menu,
	}

	menu_options[start_menu]()

	menu_rendering()

# =========Задачи==========
# . . .
# ✅ Добавить возможность записи логов вручную (ip, http-метод, путь, статус)
# ✅ Не допускать к загрузке точные копии логов (Избавится от клонирования)
# =========Доработки=======
# . . .