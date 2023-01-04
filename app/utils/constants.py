from enum import Enum


RESET_PASSWORD_SUBJECT = 'Reset Password'
EMAIL_TEMPLATE = 'password_recovery_mail.html'


class StatusType(Enum):
    ACTIVE = 1
    INACTIVE = 0


STATUS = (
    (StatusType.ACTIVE, 'Active'),
    (StatusType.INACTIVE, 'Inactive')
)


class DomainsType(Enum):
    AMAZONIA = 0
    MATA_ATLANTICA = 1
    CAATINGA = 2
    CERRADO = 3
    PANTANAL = 4
    PRADARIA = 5


DOMAINS = (
    (DomainsType.AMAZONIA, 'Amazonia'),
    (DomainsType.MATA_ATLANTICA, 'Mata Atlantica'),
    (DomainsType.CAATINGA, 'Caatinga'),
    (DomainsType.CERRADO, 'Cerrado'),
    (DomainsType.PANTANAL, 'Pantanal'),
    (DomainsType.PRADARIA, 'Pradaria'),
)


class StatesType(Enum):
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


STATES = ((StatesType.AC, 'AC'),
          (StatesType.AL, 'AL'),
          (StatesType.AP, 'AP'),
          (StatesType.AM, 'AM'),
          (StatesType.BA, 'BA'),
          (StatesType.CE, 'CE'),
          (StatesType.DF, 'DF'),
          (StatesType.ES, 'ES'),
          (StatesType.GO, 'GO'),
          (StatesType.MA, 'MA'),
          (StatesType.MG, 'MG'),
          (StatesType.MT, 'MT'),
          (StatesType.MS, 'MS'),
          (StatesType.PA, 'PA'),
          (StatesType.PE, 'PE'),
          (StatesType.PB, 'PB'),
          (StatesType.PI, 'PI'),
          (StatesType.PR, 'PR'),
          (StatesType.RJ, 'RJ'),
          (StatesType.RN, 'RN'),
          (StatesType.RR, 'RR'),
          (StatesType.RS, 'RS'),
          (StatesType.RO, 'RO'),
          (StatesType.SC, 'SC'),
          (StatesType.SE, 'SE'),
          (StatesType.SP, 'SP'),
          (StatesType.TO, 'TO'))
