import sys
import operator
import ast
import datetime
import os as py_os
import platform
import random
import time
import shutil
import json

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# --- Standard Images ---
PICS = {
    'logo': """
      ███████╗██╗  ██╗██████╗     ██████╗ ███████╗
      ██╔════╝╚██╗██╔╝██╔══██╗   ██╔═══██╗██╔════╝
      █████╗   ╚███╔╝ ██████╔╝   ██║   ██║███████╗
      ██╔══╝   ██╔██╗ ██╔═══╝    ██║   ██║╚════██║
      ███████╗██╔╝ ██╗██║        ╚██████╔╝███████║
      ╚══════╝╚═╝  ╚═╝╚═╝         ╚═════╝ ╚══════╝
    """,
    'cat': """
       /\_/\ 
      ( o.o )
       > ^ <
    """,
    'computer': """
       .---------------.
      | .------------. |
      | | OS 2026    | |
      | | SYSTEM     | |
      | '------------' |
       '---------------'
            |  |
         _.-'  '-._
        '----------'
    """
}

# --- Full Translation Dictionary ---
LANGUAGES = {
    'ru': {
        'os_name': "ЕХП ОС",
        'welcome': "С возвращением, {name}! Введите 'help' для списка команд.",
        'started': "{os_name} {version} запущена.",
        'shutdown': "Завершение работы {os_name}...",
        'restarting': "Перезагрузка {os_name}...",
        'not_found': "Ошибка: команда '{cmd}' не найдена.",
        'avail_cmd': "Доступные команды:",
        'no_help': "Нет справки для '{cmd}'.",
        'hist_empty': "История пуста.",
        'dir_empty': "Папка пуста.",
        'boot_init': "Инициализация оборудования...",
        'boot_kernel': "Загрузка ядра системы...",
        'boot_fs': "Монтирование файловой системы...",
        'boot_session': "Запуск пользовательской сессии...",
        'boot_ready': "Система готова!                   ",
        'menu_title': "--- Главное Меню ---",
        'menu_prompt': "Меню > ",
        'menu_help': "Опции: 'settings' (настройки), 'restart' (перезагрузка), 'shutdown' (выключение), 'back' (назад)",
        'set_title': "--- Настройки ---",
        'set_prompt': "Настройки > ",
        'set_help': "Опции: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Доступно: en, fr, nl, ru.\nВыберите язык: ",
        'lang_set': "Язык успешно изменен.",
        'desc_help': "Показать эту справку",
        'desc_echo': "Вывести текст на экран",
        'desc_calc': "Калькулятор (напр., calc 2+2)",
        'desc_clear': "Очистить экран",
        'desc_time': "Показать дату и время",
        'desc_history': "Показать историю команд",
        'desc_ls': "Список файлов и папок",
        'desc_game': "Игра 'Угадай число'",
        'desc_touch': "Создать пустой файл",
        'desc_cat': "Прочитать файл",
        'desc_mkdir': "Создать новую папку",
        'desc_rm': "Удалить файл или папку",
        'desc_whoami': "Показать имя пользователя",
        'desc_gallery': "Просмотр стандартных картинок",
        'desc_fmenu': "Мини-меню файлов (копировать, вставить, импорт, отмена)",
        'sys_info_title': "--- Информация о системе ---",
        'sys_storage': "--- Память и Накопители ---",
        'sys_unavailable': "Недоступно",
        'sys_ram_req': "Требуется модуль 'psutil'",
        'file_err': "Укажите имя или путь.",
        'file_not_found': "Ошибка: '{file}' не найдено.",
        'file_created': "Объект '{file}' создан.",
        'file_deleted': "Объект '{file}' удален.",
        'file_read_err': "Ошибка: {error}",
        'deploy_sys': ">>> Система Развертывания {os_name} <<<",
        'enter_user': "Введите имя пользователя системы: ",
        'user_req': "Имя пользователя обязательно.",
        'boot_title': "{os_name} Ядро v.{version}",
        'copyright': "{os_name} 2026 © Все права защищены",
        'loading': "Загрузка: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Галерея Стандартных Картинок ---",
        'gallery_prompt': "Введите имя картинки (или 'exit' для выхода): ",
        'gallery_not_found': "Картинка не найдена.",
        'fmenu_title': "--- Мини-Меню Файлов ---",
        'fmenu_opt1': "1. Создать Файл/Папку",
        'fmenu_opt2': "2. Удалить",
        'fmenu_opt3': "3. Копировать",
        'fmenu_opt4': "4. Вырезать",
        'fmenu_opt5': "5. Вставить",
        'fmenu_opt6': "6. Отменить (Доступно: {count})",
        'fmenu_opt7': "7. Вернуть (Доступно: {count})",
        'fmenu_opt8': "8. Импорт из другой ОС",
        'fmenu_opt9': "9. Обновить Экран",
        'fmenu_opt0': "0. Выход",
        'fmenu_prompt': "меню файлов > ",
        'type_file_dir': "Тип (file/dir): ",
        'name_prompt': "Имя: ",
        'target_delete': "Цель для удаления: ",
        'target_copy': "Цель для копирования: ",
        'target_cut': "Цель для вырезания: ",
        'copied_clip': "Скопировано в буфер.",
        'cut_clip': "Вырезано в буфер.",
        'clip_empty': "Буфер пуст.",
        'dest_name': "Имя назначения для '{src}': ",
        'pasted_as': "Вставлено как '{dest}'.",
        'paste_err': "Ошибка вставки: {error}",
        'nothing_undo': "Нечего отменять.",
        'undo_restored': "Отмена: Восстановлено '{orig}'",
        'undo_removed': "Отмена: Удален вставленный объект '{dest}'",
        'undo_moved': "Отмена: Объект '{dest}' перемещен обратно в '{src}'",
        'undo_fail': "Ошибка отмены: {error}",
        'nothing_redo': "Нечего возвращать.",
        'redo_del': "Возврат: Удалено '{orig}'",
        'redo_copy_warn': "Возврат для копирования не поддерживается.",
        'redo_moved': "Возврат: Перемещено из '{src}' в '{dest}'",
        'redo_fail': "Ошибка возврата: {error}",
        'import_warn': "ВНИМАНИЕ: Используйте полный путь с вашего компьютера (напр. C:\\файл.txt)",
        'import_path': "Путь в Хост-ОС: ",
        'import_succ': "Успешно импортировано '{name}'.",
        'import_err': "Ошибка импорта: {error}",
        'host_not_found': "Путь в Хост-ОС не найден.",
        'invalid_choice': "Неверный выбор.",
        'dt_title': "--- Настройки Даты и Времени ---",
        'dt_cur_time': "Текущее время системы : {time}",
        'dt_cur_tz': "Текущий часовой пояс  : UTC{tz}",
        'dt_opt1': "1. Изменить часовой пояс",
        'dt_opt2': "2. Сместить время (Добавить/Убавить часы)",
        'dt_opt3': "3. Сбросить по умолчанию",
        'dt_opt0': "0. Назад",
        'dt_choice': "Выбор: ",
        'dt_tz_prompt': "Введите смещение пояса (от -12 до +14): ",
        'dt_tz_upd': "Часовой пояс обновлен.",
        'dt_shift_prompt': "Добавить часы (отрицательное для уменьшения): ",
        'dt_shifted': "Время смещено.",
        'dt_reset': "Настройки времени сброшены.",
        'dt_invalid': "Неверный ввод.",
        'sys_build': "Версия Сборки : {version}",
        'sys_user': "Пользователь  : {user}",
        'sys_plat': "Платформа ОС  : {platform}",
        'sys_disk_tot': "Диск Всего    : {total} GB",
        'sys_disk_free': "Диск Свободно : {free} GB",
        'sys_ram_tot': "ОЗУ Всего     : {total} MB",
        'calc_usage': "Использование: calc <выражение>",
        'calc_err': "Ошибка математики: {error}",
        'game_welcome': "Угадай число (1-100). Напишите 'exit' для выхода.",
        'game_prompt': "Число > ",
        'game_high': "Выше ↑",
        'game_low': "Ниже ↓",
        'game_win': "Правильно!",
        'is_dir_err': "Это папка"
    },
    'en': {
        'os_name': "EXP OS",
        'welcome': "Welcome back, {name}! Press 'help' for the list of commands.",
        'started': "{os_name} {version} started.",
        'shutdown': "Shutting down {os_name}...",
        'restarting': "Restarting {os_name}...",
        'not_found': "Error: command '{cmd}' not found.",
        'avail_cmd': "Available Commands:",
        'no_help': "No help available for command '{cmd}'.",
        'hist_empty': "History is empty.",
        'dir_empty': "Directory is empty.",
        'boot_init': "Initializing hardware interface...",
        'boot_kernel': "Loading system kernel...",
        'boot_fs': "Mounting virtual file system...",
        'boot_session': "Starting user session...",
        'boot_ready': "System ready!                   ",
        'menu_title': "--- Main Menu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Settings Menu ---",
        'set_prompt': "Settings > ",
        'set_help': "Options: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Available: en, fr, nl, ru.\nChoose language: ",
        'lang_set': "Language successfully set.",
        'desc_help': "Show this help",
        'desc_echo': "Print the given text",
        'desc_calc': "Calculate math (e.g., calc 2+2)",
        'desc_clear': "Clear the screen",
        'desc_time': "Show current date and time",
        'desc_history': "Show command history",
        'desc_ls': "List files in current folder",
        'desc_game': "Play a number guessing game",
        'desc_touch': "Create an empty file",
        'desc_cat': "Read file content",
        'desc_mkdir': "Create a new directory",
        'desc_rm': "Remove a file or directory",
        'desc_whoami': "Display current user name",
        'desc_gallery': "View standard system pictures",
        'desc_fmenu': "Open File Mini-Menu (copy, paste, undo, import)",
        'sys_info_title': "--- System Information ---",
        'sys_storage': "--- Storage & Memory ---",
        'sys_unavailable': "Unavailable",
        'sys_ram_req': "Requires 'psutil' module",
        'file_err': "Please specify a name/path.",
        'file_not_found': "Error: '{file}' not found.",
        'file_created': "Item '{file}' created.",
        'file_deleted': "Item '{file}' deleted.",
        'file_read_err': "Error: {error}",
        'deploy_sys': ">>> {os_name} Deployment System <<<",
        'enter_user': "Enter System Username: ",
        'user_req': "Username required.",
        'boot_title': "{os_name} Core v.{version}",
        'copyright': "{os_name} 2026 © All Rights Reserved",
        'loading': "Loading: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Standard Pictures Gallery ---",
        'gallery_prompt': "Enter picture name to view (or 'exit'): ",
        'gallery_not_found': "Picture not found.",
        'fmenu_title': "--- File Mini-Menu ---",
        'fmenu_opt1': "1. Create File/Folder",
        'fmenu_opt2': "2. Delete",
        'fmenu_opt3': "3. Copy",
        'fmenu_opt4': "4. Cut",
        'fmenu_opt5': "5. Paste",
        'fmenu_opt6': "6. Undo (Available: {count})",
        'fmenu_opt7': "7. Redo (Available: {count})",
        'fmenu_opt8': "8. Import from Host OS",
        'fmenu_opt9': "9. Refresh Screen",
        'fmenu_opt0': "0. Exit",
        'fmenu_prompt': "fmenu > ",
        'type_file_dir': "Type (file/dir): ",
        'name_prompt': "Name: ",
        'target_delete': "Target to delete: ",
        'target_copy': "Target to copy: ",
        'target_cut': "Target to cut: ",
        'copied_clip': "Copied to clipboard.",
        'cut_clip': "Cut to clipboard.",
        'clip_empty': "Clipboard is empty.",
        'dest_name': "Destination name for '{src}': ",
        'pasted_as': "Pasted as '{dest}'.",
        'paste_err': "Paste Error: {error}",
        'nothing_undo': "Nothing to undo.",
        'undo_restored': "Undo: Restored '{orig}'",
        'undo_removed': "Undo: Removed pasted item '{dest}'",
        'undo_moved': "Undo: Moved '{dest}' back to '{src}'",
        'undo_fail': "Undo Failed: {error}",
        'nothing_redo': "Nothing to redo.",
        'redo_del': "Redo: Deleted '{orig}'",
        'redo_copy_warn': "Redo for copy-paste requires original file context.",
        'redo_moved': "Redo: Moved '{src}' to '{dest}'",
        'redo_fail': "Redo Failed: {error}",
        'import_warn': "WARNING: Use absolute path from your real computer (e.g. C:\\file.txt)",
        'import_path': "Host Path: ",
        'import_succ': "Successfully imported '{name}'.",
        'import_err': "Import Error: {error}",
        'host_not_found': "Host path not found.",
        'invalid_choice': "Invalid choice.",
        'dt_title': "--- Date & Time Settings ---",
        'dt_cur_time': "Current System Time : {time}",
        'dt_cur_tz': "Current Timezone    : UTC{tz}",
        'dt_opt1': "1. Change Timezone",
        'dt_opt2': "2. Shift Time (Add/Remove Hours)",
        'dt_opt3': "3. Reset to Default",
        'dt_opt0': "0. Back",
        'dt_choice': "Choice: ",
        'dt_tz_prompt': "Enter timezone offset (-12 to +14): ",
        'dt_tz_upd': "Timezone updated.",
        'dt_shift_prompt': "Add hours (negative to subtract): ",
        'dt_shifted': "Time shifted.",
        'dt_reset': "Time settings reset.",
        'dt_invalid': "Invalid input.",
        'sys_build': "Build Version  : {version}",
        'sys_user': "User           : {user}",
        'sys_plat': "OS Platform    : {platform}",
        'sys_disk_tot': "Disk Total     : {total} GB",
        'sys_disk_free': "Disk Free      : {free} GB",
        'sys_ram_tot': "RAM Total      : {total} MB",
        'calc_usage': "Usage: calc <expr>",
        'calc_err': "Math Error: {error}",
        'game_welcome': "Guess Number (1-100). Type 'exit' to quit.",
        'game_prompt': "Guess > ",
        'game_high': "Higher ↑",
        'game_low': "Lower ↓",
        'game_win': "Correct!",
        'is_dir_err': "Is a directory"
    },
    'fr': {
        'os_name': "EXP OS",
        'welcome': "Bon retour, {name}! Tapez 'help' pour la liste des commandes.",
        'started': "{os_name} {version} a démarré.",
        'shutdown': "Fermeture de {os_name}...",
        'restarting': "Redémarrage de {os_name}...",
        'not_found': "Erreur: commande '{cmd}' introuvable.",
        'avail_cmd': "Commandes disponibles:",
        'no_help': "Aucune aide disponible pour la commande '{cmd}'.",
        'hist_empty': "L'historique est vide.",
        'dir_empty': "Le répertoire est vide.",
        'boot_init': "Initialisation de l'interface matérielle...",
        'boot_kernel': "Chargement du noyau système...",
        'boot_fs': "Montage du système de fichiers...",
        'boot_session': "Démarrage de la session utilisateur...",
        'boot_ready': "Système prêt!                   ",
        'menu_title': "--- Menu Principal ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Options: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Menu des Paramètres ---",
        'set_prompt': "Paramètres > ",
        'set_help': "Options: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Disponibles: en, fr, nl, ru.\nChoisissez la langue: ",
        'lang_set': "Langue modifiée avec succès.",
        'desc_help': "Afficher cette aide",
        'desc_echo': "Imprimer le texte donné",
        'desc_calc': "Calculatrice mathématique",
        'desc_clear': "Effacer l'écran",
        'desc_time': "Afficher la date et l'heure",
        'desc_history': "Afficher l'historique des commandes",
        'desc_ls': "Lister les fichiers du dossier",
        'desc_game': "Jeu de devinettes de nombres",
        'desc_touch': "Créer un fichier vide",
        'desc_cat': "Lire le contenu d'un fichier",
        'desc_mkdir': "Créer un nouveau répertoire",
        'desc_rm': "Supprimer un fichier ou dossier",
        'desc_whoami': "Afficher le nom d'utilisateur actuel",
        'desc_gallery': "Voir les images système standard",
        'desc_fmenu': "Ouvrir le mini-menu des fichiers (copier, coller, annuler...)",
        'sys_info_title': "--- Informations Système ---",
        'sys_storage': "--- Stockage & Mémoire ---",
        'sys_unavailable': "Indisponible",
        'sys_ram_req': "Nécessite le module 'psutil'",
        'file_err': "Veuillez spécifier un nom/chemin.",
        'file_not_found': "Erreur: '{file}' introuvable.",
        'file_created': "Élément '{file}' créé.",
        'file_deleted': "Élément '{file}' supprimé.",
        'file_read_err': "Erreur: {error}",
        'deploy_sys': ">>> Système de Déploiement {os_name} <<<",
        'enter_user': "Entrez le nom d'utilisateur: ",
        'user_req': "Nom d'utilisateur requis.",
        'boot_title': "Noyau {os_name} v.{version}",
        'copyright': "{os_name} 2026 © Tous Droits Réservés",
        'loading': "Chargement: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Galerie d'Images Standard ---",
        'gallery_prompt': "Entrez le nom de l'image (ou 'exit'): ",
        'gallery_not_found': "Image introuvable.",
        'fmenu_title': "--- Mini-Menu des Fichiers ---",
        'fmenu_opt1': "1. Créer Fichier/Dossier",
        'fmenu_opt2': "2. Supprimer",
        'fmenu_opt3': "3. Copier",
        'fmenu_opt4': "4. Couper",
        'fmenu_opt5': "5. Coller",
        'fmenu_opt6': "6. Annuler (Dispo: {count})",
        'fmenu_opt7': "7. Refaire (Dispo: {count})",
        'fmenu_opt8': "8. Importer depuis l'OS Hôte",
        'fmenu_opt9': "9. Rafraîchir l'écran",
        'fmenu_opt0': "0. Quitter",
        'fmenu_prompt': "menu_fichiers > ",
        'type_file_dir': "Type (file/dir): ",
        'name_prompt': "Nom: ",
        'target_delete': "Cible à supprimer: ",
        'target_copy': "Cible à copier: ",
        'target_cut': "Cible à couper: ",
        'copied_clip': "Copié dans le presse-papiers.",
        'cut_clip': "Coupé dans le presse-papiers.",
        'clip_empty': "Presse-papiers vide.",
        'dest_name': "Nom de destination pour '{src}': ",
        'pasted_as': "Collé en tant que '{dest}'.",
        'paste_err': "Erreur de collage: {error}",
        'nothing_undo': "Rien à annuler.",
        'undo_restored': "Annuler: Restauré '{orig}'",
        'undo_removed': "Annuler: Élément collé supprimé '{dest}'",
        'undo_moved': "Annuler: Déplacé '{dest}' vers '{src}'",
        'undo_fail': "Échec de l'annulation: {error}",
        'nothing_redo': "Rien à refaire.",
        'redo_del': "Refaire: Supprimé '{orig}'",
        'redo_copy_warn': "Refaire une copie nécessite le contexte d'origine.",
        'redo_moved': "Refaire: Déplacé '{src}' vers '{dest}'",
        'redo_fail': "Échec de refaire: {error}",
        'import_warn': "ATTENTION: Utilisez le chemin absolu (ex. C:\\fichier.txt)",
        'import_path': "Chemin Hôte: ",
        'import_succ': "Importation réussie '{name}'.",
        'import_err': "Erreur d'importation: {error}",
        'host_not_found': "Chemin hôte introuvable.",
        'invalid_choice': "Choix invalide.",
        'dt_title': "--- Paramètres Date & Heure ---",
        'dt_cur_time': "Heure Système Actuelle : {time}",
        'dt_cur_tz': "Fuseau Horaire Actuel  : UTC{tz}",
        'dt_opt1': "1. Changer de Fuseau Horaire",
        'dt_opt2': "2. Décaler l'Heure (Ajouter/Soustraire)",
        'dt_opt3': "3. Réinitialiser par défaut",
        'dt_opt0': "0. Retour",
        'dt_choice': "Choix: ",
        'dt_tz_prompt': "Entrez le décalage (-12 à +14): ",
        'dt_tz_upd': "Fuseau horaire mis à jour.",
        'dt_shift_prompt': "Ajouter des heures (négatif pour soustraire): ",
        'dt_shifted': "Heure décalée.",
        'dt_reset': "Paramètres réinitialisés.",
        'dt_invalid': "Entrée invalide.",
        'sys_build': "Version Build  : {version}",
        'sys_user': "Utilisateur    : {user}",
        'sys_plat': "Plateforme OS  : {platform}",
        'sys_disk_tot': "Disque Total   : {total} GB",
        'sys_disk_free': "Disque Libre   : {free} GB",
        'sys_ram_tot': "RAM Totale     : {total} MB",
        'calc_usage': "Utilisation: calc <expr>",
        'calc_err': "Erreur Math: {error}",
        'game_welcome': "Devinez le nombre (1-100). Tapez 'exit' pour quitter.",
        'game_prompt': "Devinette > ",
        'game_high': "Plus haut ↑",
        'game_low': "Plus bas ↓",
        'game_win': "Correct!",
        'is_dir_err': "Est un dossier"
    },
    'nl': {
        'os_name': "EXP OS",
        'welcome': "Welkom terug, {name}! Typ 'help' voor de lijst met commando's.",
        'started': "{os_name} {version} is gestart.",
        'shutdown': "{os_name} afsluiten...",
        'restarting': "{os_name} herstarten...",
        'not_found': "Fout: commando '{cmd}' niet gevonden.",
        'avail_cmd': "Beschikbare Commando's:",
        'no_help': "Geen hulp beschikbaar voor commando '{cmd}'.",
        'hist_empty': "Geschiedenis is leeg.",
        'dir_empty': "Map is leeg.",
        'boot_init': "Hardware-interface initialiseren...",
        'boot_kernel': "Systeemkernel laden...",
        'boot_fs': "Virtueel bestandssysteem koppelen...",
        'boot_session': "Gebruikerssessie starten...",
        'boot_ready': "Systeem gereed!                   ",
        'menu_title': "--- Hoofdmenu ---",
        'menu_prompt': "Menu > ",
        'menu_help': "Opties: 'settings', 'restart', 'shutdown', 'back'",
        'set_title': "--- Instellingen ---",
        'set_prompt': "Instellingen > ",
        'set_help': "Opties: 'sysinfo', 'lang', 'datetime', 'back'",
        'lang_choose': "Beschikbaar: en, fr, nl, ru.\nKies taal: ",
        'lang_set': "Taal succesvol ingesteld.",
        'desc_help': "Toon deze hulp",
        'desc_echo': "Druk de gegeven tekst af",
        'desc_calc': "Rekenmachine (bijv. calc 2+2)",
        'desc_clear': "Wis het scherm",
        'desc_time': "Toon huidige datum en tijd",
        'desc_history': "Toon commandogeschiedenis",
        'desc_ls': "Lijst bestanden in huidige map",
        'desc_game': "Speel een getallenraadspel",
        'desc_touch': "Maak een leeg bestand",
        'desc_cat': "Lees bestandsinhoud",
        'desc_mkdir': "Maak een nieuwe map",
        'desc_rm': "Verwijder een bestand of map",
        'desc_whoami': "Toon huidige gebruikersnaam",
        'desc_gallery': "Bekijk standaard systeemafbeeldingen",
        'desc_fmenu': "Open Bestandsmenu (kopiëren, plakken, ongedaan maken...)",
        'sys_info_title': "--- Systeeminformatie ---",
        'sys_storage': "--- Opslag & Geheugen ---",
        'sys_unavailable': "Niet beschikbaar",
        'sys_ram_req': "Vereist 'psutil' module",
        'file_err': "Geef een naam/pad op.",
        'file_not_found': "Fout: '{file}' niet gevonden.",
        'file_created': "Item '{file}' aangemaakt.",
        'file_deleted': "Item '{file}' verwijderd.",
        'file_read_err': "Fout: {error}",
        'deploy_sys': ">>> {os_name} Implementatiesysteem <<<",
        'enter_user': "Voer Systeemgebruikersnaam in: ",
        'user_req': "Gebruikersnaam vereist.",
        'boot_title': "{os_name} Kern v.{version}",
        'copyright': "{os_name} 2026 © Alle Rechten Voorbehouden",
        'loading': "Laden: [{bar}] {pct}% | {status}",
        'gallery_title': "--- Standaard Afbeeldingengalerij ---",
        'gallery_prompt': "Voer afbeeldingsnaam in (of 'exit'): ",
        'gallery_not_found': "Afbeelding niet gevonden.",
        'fmenu_title': "--- Bestandsmenu ---",
        'fmenu_opt1': "1. Maak Bestand/Map",
        'fmenu_opt2': "2. Verwijderen",
        'fmenu_opt3': "3. Kopiëren",
        'fmenu_opt4': "4. Knippen",
        'fmenu_opt5': "5. Plakken",
        'fmenu_opt6': "6. Ongedaan maken (Beschikbaar: {count})",
        'fmenu_opt7': "7. Opnieuw doen (Beschikbaar: {count})",
        'fmenu_opt8': "8. Importeren vanuit Host OS",
        'fmenu_opt9': "9. Scherm Vernieuwen",
        'fmenu_opt0': "0. Afsluiten",
        'fmenu_prompt': "bestandsmenu > ",
        'type_file_dir': "Type (file/dir): ",
        'name_prompt': "Naam: ",
        'target_delete': "Doel om te verwijderen: ",
        'target_copy': "Doel om te kopiëren: ",
        'target_cut': "Doel om te knippen: ",
        'copied_clip': "Gekopieerd naar klembord.",
        'cut_clip': "Geknipt naar klembord.",
        'clip_empty': "Klembord is leeg.",
        'dest_name': "Bestemmingsnaam voor '{src}': ",
        'pasted_as': "Geplakt als '{dest}'.",
        'paste_err': "Plakfout: {error}",
        'nothing_undo': "Niets ongedaan te maken.",
        'undo_restored': "Ongedaan: Hersteld '{orig}'",
        'undo_removed': "Ongedaan: Geplakt item verwijderd '{dest}'",
        'undo_moved': "Ongedaan: Verplaatst '{dest}' terug naar '{src}'",
        'undo_fail': "Ongedaan maken mislukt: {error}",
        'nothing_redo': "Niets opnieuw te doen.",
        'redo_del': "Opnieuw: Verwijderd '{orig}'",
        'redo_copy_warn': "Opnieuw kopiëren vereist de oorspronkelijke context.",
        'redo_moved': "Opnieuw: Verplaatst '{src}' naar '{dest}'",
        'redo_fail': "Opnieuw doen mislukt: {error}",
        'import_warn': "WAARSCHUWING: Gebruik absoluut pad (bijv. C:\\bestand.txt)",
        'import_path': "Host Pad: ",
        'import_succ': "Succesvol geïmporteerd '{name}'.",
        'import_err': "Importfout: {error}",
        'host_not_found': "Host pad niet gevonden.",
        'invalid_choice': "Ongeldige keuze.",
        'dt_title': "--- Datum & Tijd Instellingen ---",
        'dt_cur_time': "Huidige Systeemtijd : {time}",
        'dt_cur_tz': "Huidige Tijdzone    : UTC{tz}",
        'dt_opt1': "1. Verander Tijdzone",
        'dt_opt2': "2. Tijd Verschuiven (Uren)",
        'dt_opt3': "3. Reset naar Standaard",
        'dt_opt0': "0. Terug",
        'dt_choice': "Keuze: ",
        'dt_tz_prompt': "Voer tijdzone offset in (-12 tot +14): ",
        'dt_tz_upd': "Tijdzone bijgewerkt.",
        'dt_shift_prompt': "Uren toevoegen (negatief voor aftrekken): ",
        'dt_shifted': "Tijd verschoven.",
        'dt_reset': "Tijdinstellingen gereset.",
        'dt_invalid': "Ongeldige invoer.",
        'sys_build': "Bouwversie     : {version}",
        'sys_user': "Gebruiker      : {user}",
        'sys_plat': "OS Platform    : {platform}",
        'sys_disk_tot': "Schijf Totaal  : {total} GB",
        'sys_disk_free': "Schijf Vrij    : {free} GB",
        'sys_ram_tot': "RAM Totaal     : {total} MB",
        'calc_usage': "Gebruik: calc <expr>",
        'calc_err': "Reken Fout: {error}",
        'game_welcome': "Raad het getal (1-100). Typ 'exit' om te stoppen.",
        'game_prompt': "Gok > ",
        'game_high': "Hoger ↑",
        'game_low': "Lager ↓",
        'game_win': "Correct!",
        'is_dir_err': "Is een map"
    }
}


class EXPOS:
    def __init__(self):
        self.running = True
        self.is_restarting = False
        self.version = "alpha 0.0.2"
        self.history = []
        self.username = "User"
        self.lang = "ru"
        self.config_file = ".expos_config"
        self.trash_dir = ".expos_trash"

        self.tz_offset_hours = 0
        self.time_offset_seconds = 0

        self.clipboard = None
        self.undo_stack = []
        self.redo_stack = []

        self.commands = {
            'help': self.cmd_help,
            'menu': self.cmd_menu,
            'echo': self.cmd_echo,
            'calc': self.cmd_calc,
            'clear': self.cmd_clear,
            'time': self.cmd_time,
            'history': self.cmd_history,
            'ls': self.cmd_ls,
            'game': self.cmd_game,
            'touch': self.cmd_touch,
            'cat': self.cmd_cat,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'whoami': self.cmd_whoami,
            'gallery': self.cmd_gallery,
            'fmenu': self.cmd_fmenu
        }

    @property
    def help_text(self):
        return {k: self.t(f'desc_{k}') for k in self.commands.keys()}

    def t(self, key, **kwargs):
        text = LANGUAGES.get(self.lang, LANGUAGES['en']).get(key, LANGUAGES['en'].get(key, key))
        return text.format(**kwargs) if kwargs else text

    def get_current_time(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours=self.tz_offset_hours,
                                                             seconds=self.time_offset_seconds)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def load_config(self):
        try:
            py_os.makedirs(self.trash_dir, exist_ok=True)
        except:
            pass

        if py_os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.loads(f.read().strip())
                    self.username = config.get('username', 'User')
                    self.lang = config.get('lang', 'ru')
                    self.tz_offset_hours = config.get('tz_hours', 0)
                    self.time_offset_seconds = config.get('t_secs', 0)
            except:
                pass
        else:
            self.run_installation()

    def save_config(self):
        config = {
            'username': self.username, 'lang': self.lang,
            'tz_hours': self.tz_offset_hours, 't_secs': self.time_offset_seconds
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)
        except:
            pass

    def run_installation(self):
        self.cmd_clear("")
        print(self.t('deploy_sys', os_name=self.t('os_name')))
        time.sleep(0.5)
        while True:
            name = input(self.t('enter_user')).strip()
            if name:
                self.username = name
                break
            print(self.t('user_req'))
        self.lang = "ru"
        self.save_config()
        self.cmd_clear("")

    def boot_sequence(self):
        self.cmd_clear("")
        print(self.t('boot_title', os_name=self.t('os_name'), version=self.version))
        print(self.t('copyright', os_name=self.t('os_name')) + "\n")

        for i in range(1, 101):
            blocks = int((i / 100) * 30)
            # ВАЖНО: Заменено на обычные символы, чтобы терминал не вылетал из-за UnicodeEncodeError
            bar = '#' * blocks + '-' * (30 - blocks)

            if i < 30:
                status = self.t('boot_init')
            elif i < 60:
                status = self.t('boot_kernel')
            elif i < 85:
                status = self.t('boot_fs')
            else:
                status = self.t('boot_session')

            sys.stdout.write(f"\r" + self.t('loading', bar=bar, pct=i, status=status))
            sys.stdout.flush()
            time.sleep(random.uniform(0.005, 0.02))

        print(f"\n\n{self.t('boot_ready')}")
        time.sleep(0.5)
        self.cmd_clear("")

    def print_taskbar(self):
        width = 70
        print("=" * width)
        tz_str = f"UTC{'+' + str(self.tz_offset_hours) if self.tz_offset_hours >= 0 else self.tz_offset_hours}"
        info = f" {self.get_current_time()} | {self.username} | {tz_str} "
        os_n = self.t('os_name')
        print(f"| {os_n} 2026 {info:>{width - len(os_n) - 9}}|")
        print("=" * width)

    def start(self):
        self.load_config()
        self.boot_sequence()
        self.print_taskbar()
        print(self.t('started', os_name=self.t('os_name'), version=self.version))
        print(self.t('welcome', name=self.username))

        while self.running:
            try:
                user_input = input(f"[{self.username}@expos ~]$ ").strip()
                if not user_input: continue
                self.history.append(user_input)
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                self.cmd_shutdown("")

    def execute_command(self, command_line):
        parts = command_line.split(' ', 1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(self.t('not_found', cmd=cmd))

    # --- Core Commands ---
    def cmd_help(self, args):
        print("\n" + self.t('copyright', os_name=self.t('os_name')))
        print(f"{self.t('avail_cmd')}")
        for cmd, desc in self.help_text.items():
            print(f"  {cmd:<10} : {desc}")

    def cmd_echo(self, args):
        print(args)

    def cmd_time(self, args):
        print(self.get_current_time())

    def cmd_history(self, args):
        if not self.history:
            print(self.t('hist_empty'))
        else:
            for i, cmd in enumerate(self.history, 1): print(f"{i:3}: {cmd}")

    def cmd_whoami(self, args):
        print(self.username)

    def cmd_gallery(self, args):
        print(self.t('gallery_title'))
        for name in PICS.keys():
            print(f"- {name}")
        choice = input(self.t('gallery_prompt')).strip().lower()
        if choice in PICS:
            print(PICS[choice])
        elif choice != 'exit':
            print(self.t('gallery_not_found'))

    # --- FS Commands ---
    def cmd_ls(self, args):
        try:
            files = [f for f in py_os.listdir('.') if f != self.trash_dir and not f.startswith('.expos')]
            if not files:
                print(self.t('dir_empty'))
            else:
                for f in sorted(files):
                    tag = "[DIR] " if py_os.path.isdir(f) else "[FILE]"
                    print(f"{tag} {f}")
        except Exception as e:
            print(f"FS Error: {e}")

    def cmd_mkdir(self, args):
        if not args: print(self.t('file_err')); return
        try:
            py_os.makedirs(args, exist_ok=True); print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_rm(self, args):
        if not args: print(self.t('file_err')); return
        if not py_os.path.exists(args): print(self.t('file_not_found', file=args)); return
        try:
            trash_path = py_os.path.join(self.trash_dir, f"{int(time.time())}_{py_os.path.basename(args)}")
            shutil.move(args, trash_path)
            self.undo_stack.append({'action': 'delete', 'orig': args, 'trash': trash_path})
            self.redo_stack.clear()
            print(self.t('file_deleted', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_touch(self, args):
        if not args: print(self.t('file_err')); return
        try:
            with open(args, 'a'):
                pass
            print(self.t('file_created', file=args))
        except Exception as e:
            print(self.t('file_read_err', error=e))

    def cmd_cat(self, args):
        if not args: print(self.t('file_err')); return
        if not py_os.path.exists(args): print(self.t('file_not_found', file=args)); return
        if py_os.path.isdir(args): print(self.t('file_read_err', error=self.t('is_dir_err'))); return
        try:
            with open(args, 'r', encoding='utf-8') as f:
                print(f.read())
        except Exception as e:
            print(self.t('file_read_err', error=e))

    # --- File Mini-Menu ---
    def cmd_fmenu(self, args):
        while True:
            print(f"\n{self.t('fmenu_title')}")
            print(self.t('fmenu_opt1'))
            print(self.t('fmenu_opt2'))
            print(self.t('fmenu_opt3'))
            print(self.t('fmenu_opt4'))
            print(self.t('fmenu_opt5'))
            print(self.t('fmenu_opt6', count=len(self.undo_stack)))
            print(self.t('fmenu_opt7', count=len(self.redo_stack)))
            print(self.t('fmenu_opt8'))
            print(self.t('fmenu_opt9'))
            print(self.t('fmenu_opt0'))

            choice = input(self.t('fmenu_prompt')).strip()

            if choice == '1':
                t = input(self.t('type_file_dir')).strip().lower()
                n = input(self.t('name_prompt')).strip()
                if t == 'dir':
                    self.cmd_mkdir(n)
                else:
                    self.cmd_touch(n)

            elif choice == '2':
                self.cmd_rm(input(self.t('target_delete')).strip())

            elif choice == '3':
                src = input(self.t('target_copy')).strip()
                if py_os.path.exists(src):
                    self.clipboard = ('copy', src)
                    print(self.t('copied_clip'))
                else:
                    print(self.t('file_not_found', file=src))

            elif choice == '4':
                src = input(self.t('target_cut')).strip()
                if py_os.path.exists(src):
                    self.clipboard = ('cut', src)
                    print(self.t('cut_clip'))
                else:
                    print(self.t('file_not_found', file=src))

            elif choice == '5':
                if not self.clipboard:
                    print(self.t('clip_empty'))
                else:
                    mode, src = self.clipboard
                    dest = input(self.t('dest_name', src=src)).strip()
                    try:
                        if mode == 'copy':
                            if py_os.path.isdir(src):
                                shutil.copytree(src, dest)
                            else:
                                shutil.copy2(src, dest)
                            self.undo_stack.append({'action': 'paste_copy', 'dest': dest})
                        elif mode == 'cut':
                            shutil.move(src, dest)
                            self.undo_stack.append({'action': 'paste_cut', 'src': src, 'dest': dest})
                            self.clipboard = None
                        self.redo_stack.clear()
                        print(self.t('pasted_as', dest=dest))
                    except Exception as e:
                        print(self.t('paste_err', error=e))

            elif choice == '6':  # UNDO
                if not self.undo_stack:
                    print(self.t('nothing_undo'))
                else:
                    act = self.undo_stack.pop()
                    try:
                        if act['action'] == 'delete':
                            shutil.move(act['trash'], act['orig'])
                            self.redo_stack.append(act)
                            print(self.t('undo_restored', orig=act['orig']))
                        elif act['action'] == 'paste_copy':
                            if py_os.path.isdir(act['dest']):
                                shutil.rmtree(act['dest'])
                            else:
                                py_os.remove(act['dest'])
                            self.redo_stack.append(act)
                            print(self.t('undo_removed', dest=act['dest']))
                        elif act['action'] == 'paste_cut':
                            shutil.move(act['dest'], act['src'])
                            self.redo_stack.append(act)
                            print(self.t('undo_moved', dest=act['dest'], src=act['src']))
                    except Exception as e:
                        print(self.t('undo_fail', error=e))

            elif choice == '7':  # REDO
                if not self.redo_stack:
                    print(self.t('nothing_redo'))
                else:
                    act = self.redo_stack.pop()
                    try:
                        if act['action'] == 'delete':
                            shutil.move(act['orig'], act['trash'])
                            self.undo_stack.append(act)
                            print(self.t('redo_del', orig=act['orig']))
                        elif act['action'] == 'paste_copy':
                            print(self.t('redo_copy_warn'))
                        elif act['action'] == 'paste_cut':
                            shutil.move(act['src'], act['dest'])
                            self.undo_stack.append(act)
                            print(self.t('redo_moved', src=act['src'], dest=act['dest']))
                    except Exception as e:
                        print(self.t('redo_fail', error=e))

            elif choice == '8':  # IMPORT
                print(self.t('import_warn'))
                host_path = input(self.t('import_path')).strip()
                if py_os.path.exists(host_path):
                    try:
                        basename = py_os.path.basename(host_path)
                        if py_os.path.isdir(host_path):
                            shutil.copytree(host_path, basename)
                        else:
                            shutil.copy2(host_path, basename)
                        print(self.t('import_succ', name=basename))
                    except Exception as e:
                        print(self.t('import_err', error=e))
                else:
                    print(self.t('host_not_found'))

            elif choice == '9':
                self.cmd_clear("")
                self.print_taskbar()
            elif choice == '0' or choice == 'exit':
                break
            else:
                print(self.t('invalid_choice'))

    # --- System & Menus ---
    def cmd_menu(self, args):
        print(f"\n{self.t('menu_title')}\n{self.t('menu_help')}")
        while self.running:
            cmd = input(self.t('menu_prompt')).strip().lower()
            if cmd in ['back', 'exit']:
                break
            elif cmd == 'settings':
                self.cmd_settings("")
            elif cmd == 'restart':
                self.cmd_restart("")
            elif cmd == 'shutdown':
                self.cmd_shutdown("")

    def cmd_settings(self, args):
        print(f"\n{self.t('set_title')}\n{self.t('set_help')}")
        while self.running:
            cmd = input(self.t('set_prompt')).strip().lower()
            if cmd in ['back', 'exit']:
                break
            elif cmd == 'sysinfo':
                self.run_sysinfo()
            elif cmd == 'lang':
                self.run_lang()
            elif cmd == 'datetime':
                self.run_datetime_settings()

    def run_datetime_settings(self):
        print(f"\n{self.t('dt_title')}")
        print(self.t('dt_cur_time', time=self.get_current_time()))
        print(self.t('dt_cur_tz',
                     tz=f"{'+' + str(self.tz_offset_hours) if self.tz_offset_hours >= 0 else self.tz_offset_hours}"))
        print(self.t('dt_opt1'))
        print(self.t('dt_opt2'))
        print(self.t('dt_opt3'))
        print(self.t('dt_opt0'))

        c = input(self.t('dt_choice')).strip()
        if c == '1':
            try:
                self.tz_offset_hours = int(input(self.t('dt_tz_prompt')).strip())
                self.save_config()
                print(self.t('dt_tz_upd'))
            except:
                print(self.t('dt_invalid'))
        elif c == '2':
            try:
                h = int(input(self.t('dt_shift_prompt')).strip())
                self.time_offset_seconds += h * 3600
                self.save_config()
                print(self.t('dt_shifted'))
            except:
                print(self.t('dt_invalid'))
        elif c == '3':
            self.tz_offset_hours = 0
            self.time_offset_seconds = 0
            self.save_config()
            print(self.t('dt_reset'))

    def run_sysinfo(self):
        print(f"\n{self.t('sys_info_title')}")
        print(self.t('sys_build', version=self.version))
        print(self.t('sys_user', user=self.username))
        print(self.t('sys_plat', platform=f"{platform.system()} {platform.release()}"))
        print(self.t('sys_storage'))
        try:
            total, used, free = shutil.disk_usage(py_os.path.abspath(py_os.sep))
            print(self.t('sys_disk_tot', total=total // (2 ** 30)))
            print(self.t('sys_disk_free', free=free // (2 ** 30)))
        except:
            print(f"Disk           : {self.t('sys_unavailable')}")

        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            print(self.t('sys_ram_tot', total=mem.total // (2 ** 20)))
        else:
            print(f"RAM            : {self.t('sys_ram_req')}")

    def run_lang(self):
        new_lang = input(self.t('lang_choose')).strip().lower()
        if new_lang in LANGUAGES:
            self.lang = new_lang
            self.save_config()
            print(self.t('lang_set'))
        else:
            print(self.t('dt_invalid'))

    def cmd_shutdown(self, args):
        print(self.t('shutdown', os_name=self.t('os_name')))
        time.sleep(1)
        self.running = False

    def cmd_restart(self, args):
        print(self.t('restarting', os_name=self.t('os_name')))
        time.sleep(1)
        self.running = False
        self.is_restarting = True

    def cmd_calc(self, args):
        if not args: print(self.t('calc_usage')); return
        try:
            print(self.safe_eval(args))
        except Exception as e:
            print(self.t('calc_err', error=e))

    def safe_eval(self, expression):
        operators = {
            ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
            ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos
        }

        def _eval(node):
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.BinOp):
                return operators[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp):
                return operators[type(node.op)](_eval(node.operand))
            raise ValueError("Unsupported Operation")

        tree = ast.parse(expression, mode='eval')
        return _eval(tree.body)

    def cmd_clear(self, args):
        py_os.system('cls' if platform.system() == "Windows" else 'clear')

    def cmd_game(self, args):
        number = random.randint(1, 100)
        print(self.t('game_welcome'))
        while True:
            inp = input(self.t('game_prompt')).strip().lower()
            if inp == 'exit': break
            if not inp.isdigit(): continue
            guess = int(inp)
            if guess < number:
                print(self.t('game_high'))
            elif guess > number:
                print(self.t('game_low'))
            else:
                print(self.t('game_win')); break


# Защита от вылетов: Если произойдет любая критическая ошибка,
# окно консоли не закроется моментально.
if __name__ == "__main__":
    try:
        while True:
            os_instance = EXPOS()
            os_instance.start()
            if not os_instance.is_restarting:
                break
    except Exception as error_msg:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА / CRITICAL ERROR]: {error_msg}")
        input("Нажмите Enter для выхода / Press Enter to exit...")