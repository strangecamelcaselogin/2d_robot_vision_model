SETTINGS_NAME = 'settings'


class SettingsStorage:
    '''
    Store your settings with access through the point
    Настройки с доступом через точку
    '''
    def __init__(self, path):
        self.__dict__['path'] = path

        try:
            f = open(self.path, 'r')
            self.__dict__.update(eval(f.read()))

        except Exception as e:
            print(e)

        finally:
            f.close()

    def __setattr__(self, key, value):
        self.__dict__.update({key, value})

    def save(self):
        f = open(self.path, 'w')
        f.write(repr(self.__dict__))
        f.close()


if __name__ == '__main__':
    print('test branch')
    c = SettingsStorage(SETTINGS_NAME)
    for key, value in c.__dict__.items():
        print(key, '=', value)

else:
    settings = SettingsStorage(SETTINGS_NAME)
