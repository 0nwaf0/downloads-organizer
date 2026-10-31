import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

downloads_path = os.path.expanduser('~/Downloads')

# خريطة التصنيفات: تربط كل امتداد بالمجلد المناسب
# (يدعم الأسماء التي طلبتها: صور، فيديو، مستندات، موسيقى، وغيرها)
EXTENSIONS = {
    'صور': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
    'Pictures': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
    
    'مستندات': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.odt'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.odt'],
    
    'فيديو': ['.mp4', '.mkv', '.avi', '.mov', '.webm'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.webm'],
    
    'موسيقى': ['.mp3', '.wav', '.flac', '.aac'],
    'Music': ['.mp3', '.wav', '.flac', '.aac'],
    
    'ملفات مضغوطة': ['.zip', '.tar', '.gz', '.7z', '.rar'],
    'Archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
    
    'برامج': ['.deb', '.sh', '.run', '.AppImage'],
    'Programs': ['.deb', '.sh', '.run', '.AppImage']
}

def organize_file(file_path):
    if os.path.isdir(file_path):
        return
    
    filename = os.path.basename(file_path)
    file_ext = os.path.splitext(filename)[1].lower()

    for folder_name, extensions in EXTENSIONS.items():
        if file_ext in extensions:
            target_folder = os.path.join(downloads_path, folder_name)
            os.makedirs(target_folder, exist_ok=True)
            
            destination = os.path.join(target_folder, filename)
            # تجنب تداخل الأسماء لو الملف موجود مسبقاً
            if not os.path.exists(destination) and file_path != destination:
                shutil.move(file_path, destination)
                print(f"تم نقل الملف: {filename} -> {folder_name}")
            break

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)
            organize_file(event.src_path)

if __name__ == '__main__':
    print("جاري فحص وترتيب الملفات الحالية في التنزيلات...")
    for filename in os.listdir(downloads_path):
        organize_file(os.path.join(downloads_path, filename))

    print(f"\n الأداة تعمل الآن في الخلفية وتراقب مجلد التنزيلات (اضغط Ctrl + C للإيقاف)...")
    
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
