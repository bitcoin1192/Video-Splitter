import requests

def main():
    try:
        colar = requests.get('api.sisalma.com/create')
        requests.get('api.sisalma.com/start')
    except:
        pass

if __name__ == '__main__':
    main()