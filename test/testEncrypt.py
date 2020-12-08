import GlobalVar


if __name__ == '__main__':
    pYpwd=GlobalVar.cf.get('workShop', 'tj.userName')
    pTpwd=GlobalVar.cf.get('workShop', 'tj.pwd')

    print(GlobalVar.decrypt(pYpwd))
    print(GlobalVar.decrypt(pTpwd))
#