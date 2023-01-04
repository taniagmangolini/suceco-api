from enumchoicefield import ChoiceEnum


RESET_PASSWORD_SUBJECT = 'Reset Password'
EMAIL_TEMPLATE = 'password_recovery_mail.html'


class StatusType(ChoiceEnum):
    active = 'Active'
    inactive = 'Inactive'


class DomainsType(ChoiceEnum):
    amazonia = 'Amazonia'
    mata_atlantica = 'Mata Atlantica'
    caatinga = 'Caatinga'
    cerrado = 'Cerrado'
    pantanal = 'Pantanal'
    pradaria = 'Pradaria'


class StatesType(ChoiceEnum):
    AC = 0
    AL = 1
    AP = 2
    AM = 3
    BA = 4
    CE = 5
    DF = 6
    ES = 7
    GO = 8
    MA = 9
    MG = 10
    MT = 11
    MS = 12
    PA = 13
    PE = 14
    PB = 15
    PI = 16
    PR = 17
    RJ = 18
    RN = 19
    RR = 20
    RO = 21
    RS = 22
    SC = 23
    SE = 24
    SP = 25
    TO = 26
