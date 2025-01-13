class ColorLogger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def info(message: str):
        print(f"{ColorLogger.OKBLUE}[INFO] {message}{ColorLogger.ENDC}")

    @staticmethod
    def success(message: str):
        print(f"{ColorLogger.OKGREEN}[SUCCESS] {message}{ColorLogger.ENDC}")

    @staticmethod
    def warning(message: str):
        print(f"{ColorLogger.WARNING}[WARNING] {message}{ColorLogger.ENDC}")

    @staticmethod
    def error(message: str):
        print(f"{ColorLogger.FAIL}[ERROR] {message}{ColorLogger.ENDC}")

    @staticmethod
    def debug(message: str):
        print(f"{ColorLogger.HEADER}[DEBUG] {message}{ColorLogger.ENDC}")