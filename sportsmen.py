class Sportsmen():
    # установка
    def set_All(self):
        Fam = input('Введите фамилию спортсмена: ')
        Name = input('Введите организацию спортсмена: ')
        while 1:
            try:
                Short = float(input('Введите время пробега кор. дист-ии(с): '))
                break
            except ValueError:
                print('Вводите только цифры!')
        while 1:
            try:
                Long = float(input('Введите время пробега длин. дист-ии(м.с): '))
                break
            except ValueError:
                print('Вводите только цифры')
        while 1:
            try:
                speed_Short = float(input('Введите скорость уч-ника на кор. дист-ии(м/с): '))
                break
            except ValueError:
                print('Вводите только цифры')
        self.Fam = Fam
        self.Name = Name
        self.Short = Short
        self.Long = Long

    # вывод
    def set_Fam(self, Fam):
        self.Fam = Fam

    def set_Name(self, Name):
        self.Name = Name

    def set_Short(self, Short):
        self.Short = Short

    def set_Long(self, Long):
        self.Long = Long

    def get_Fam(self):
        return self.Fam

    def get_Name(self):
        return self.Name

    def get_Short(self):
        return self.Short

    def get_Long(self):
        return self.Long

    def get_All(self):
        print('Фамилия:', self.Fam)
        print('Наименование орг-ии:', self.Name)
        print('Время пробега кор. дист-ии(с):', self.Short)
        print('Время пробега длин. дист-ии(м.с):', self.Long)

    # конструктор
    def __init__(self):
        pass
