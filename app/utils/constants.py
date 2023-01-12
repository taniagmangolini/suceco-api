from enum import Enum


RESET_PASSWORD_SUBJECT = 'Reset Password'

EMAIL_TEMPLATE = 'password_recovery_mail.html'


class DomainType(Enum):
    AMAZONIA = 0
    MATA_ATLANTICA = 1
    CAATINGA = 2
    CERRADO = 3
    PANTANAL = 4
    PRADARIA = 5
    OTHER = 6


class StateType(Enum):
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


class StageType(Enum):
    PIONEIRA = 0
    SECUNDARIA_INICIAL = 1
    SECUNDARIA_TARDIA = 2
    UMBROFILA = 3
    SECUNDARIA = 4
    CLIMACICA = 5
