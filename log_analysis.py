from time import sleep

requests = []

# -------------------------------------------UI--------------------------------------------
def menu_rendering():
	print("\n           📊 Анализатор логов\n")
	print('''1. Вывести всю активность\n2. Все запросы (Успешные/Перенаправления/Ошибки)\n3. Фильтрация по колонкам\n0. Закрыть''')
	print("------------------------")

	global start_menu

	start_menu = int(input("Выберите пункт меню: "))

def rendering_table_of_ip():
	print('---------------------------------------------------------')
	print(f'''ID | IP           | METHOD | PATH      | STATUS''')
	print('---------------------------------------------------------')
# -----------------------------------------------------------------------------------------

# ----------------------------------------FUNCTIONS----------------------------------------
def load_logs():
	request_id = 0

	with open('log.txt') as file:
		for line in file.readlines():
			line = line.strip().split()
			request_id += 1
			requests.append(dict(ID=request_id, ip=line[0], method=line[1], path=line[2], status=int(line[3])))

def get_unique_ips():
	unique_ips = {data['ip'] for data in requests}

	return unique_ips

def get_ips_only():
	print('-----------------')
	print('ID | IP |')
	print('-----------------')
	
	request_id = 0

	for ip in get_unique_ips():
		request_id += 1
		print(f'{str(request_id).ljust(2)} | {ip}')
		sleep(0.5)

def show_all_logs():
	rendering_table_of_ip()

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
	get_ips_only()

	select_ip = int(input("Выберите IP адрес для фильтрации: "))

	request_id = 0

	found_ip = ""

	for ip in get_unique_ips():
		request_id += 1
		
		if select_ip == request_id:
			found_ip = ip
			break

	if found_ip != "":
		rendering_table_of_ip()

		for data in requests:
			if data["ip"] == found_ip:
				print(f"{str(data['ID']).ljust(2)} | {data['ip'].ljust(12)} | {data['method'].ljust(6)} | {data['path'].ljust(9)} | {data['status']}")
				sleep(0.5)
	else:
		print("Ошибка! Выберите IP из списка.")
	print('---------------------------------------------------------')
	input("Нажмите Enter, чтобы продолжить...")

def show_top_paths():
	paths = [data['path'] for data in requests]

	for i in range(0, len(paths) - 1):
		if paths.count(paths[i]) < paths.count(paths[i + 1]):
			paths[i], paths[i + 1] = paths[i + 1], paths[i]

	paths = sorted(set(paths))

	print('---------------------------')
	print('ID |   PATH   | TOTAL_REQUESTS')
	print('---------------------------')
	sleep(0.5)
	
	path_id = 0

	for path in paths:
		path_id += 1
		print(f"{str(path_id).ljust(2)} | {path.ljust(8)} | {[data['path'] for data in requests].count(path)}")
		sleep(0.5)
	print('-----------------')
	input("Нажмите Enter, чтобы продолжить...")
# -------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
load_logs()
menu_rendering()

while start_menu != 0:

	# Вывод всей активности (Всего содержимого файла log.txt)
	if start_menu == 1:
		show_all_logs()

	elif start_menu == 2:
		show_status_stats()

	# Фильтрация по колонкам
	elif start_menu == 3:
		print('------------------------')
		print('1. Все IP адреса (без повторений)')
		print('2. Активность конкретного IP (Фильтрация)')
		print('3. ТОП-страниц по запросам')
		print('------------------------')

		choice = int(input("Выберите опцию: "))

		if choice == 1:
			get_ips_only()

		elif choice == 2:
			get_one_ip_stats()

		elif choice == 3:
			show_top_paths()

	menu_rendering()
