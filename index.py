from settings.router import Router

routing = Router()
routing.AddRoute('DaftarLogin','controller.DaftarLoginController','daftarloginController')
routing.AddRoute('login','controller.LoginController','loginController')
routing.AddRoute('temenlah','controller.AddfriendController','addFriendController')
routing.AddRoute('chat','controller.NewchatController','newchatController')