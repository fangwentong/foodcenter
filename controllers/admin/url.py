#!/usr/bin/env python2
# coding=utf-8

prefix = "controllers.admin."

urls = (
    r"", prefix + "admin.Index",
    r"/", prefix + "admin.Index",

    r"/login", prefix + "admin.LogIn",
    r"/logout", prefix + "admin.LogOut",
    r"/profile", prefix + "admin.GetProfile",
    r"/settings", prefix + "admin.ChgPasswd",

    r"/dashboard", prefix + "admin.DashBoard",
    r"/orderings", prefix + "admin.Orderings",
    r"/articles", prefix + "admin.ArticleManagement",
    r"/meals", prefix + "admin.GetMeals",
    r"/addmeal", prefix + "admin.AddMeal",
    r"/feedback", prefix + "admin.FeedbackManagement",
    r"/users", prefix + "admin.Users",
    r"/adduser", prefix + "admin.AddUser",

    r"/tools", prefix + "admin.ToolsList",
    r"/tools/draw-prize", prefix + "admin.DrawPrize",
    r"/tools/add-order", prefix + "admin.AddOrder",
    r"/tools/search-order", prefix + "admin.SearchOrder"

)
