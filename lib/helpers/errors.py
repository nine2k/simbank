class PrivilegeError(Exception):
    ''' raise this for unprviledged attempt '''

class ProgramTermination(Exception):
    ''' raise this to stop program '''

class AccountNotFound(Exception):
    ''' raise this when account is not found '''

class BackendConstraintError(Exception):
    ''' raise this when backend encountered a constraint violation '''
