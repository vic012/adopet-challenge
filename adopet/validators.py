import re 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
      
def check(email):
    """
    Parte dste código é de autroia do site:
    https://acervolima.com/verifique-se-o-endereco-de-e-mail-e-valido-ou-nao-em-python/
    """
    if(re.search(regex,email)):  
        return True
    return False

def valid_password(password, confirm_password):
    if password != confirm_password:
        return False
    return True