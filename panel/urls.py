from django.urls import path
from .views import *
urlpatterns = [
    path("getUsers", get_users),
    path("loadProfile", load_profile_based_on_id),
    path("recordChangesOfProfile", recordChangesOfProfile),
    path("loadProfileFriends", loadProfileFriends),
    path("sortLotteryBasedOnHighest", sortLotteryBasedOnHighest),
    path("modalHandlerLotteryProfile", modalHandlerLotteryProfile),
    path("modalHandlerLotteryWinningProfile", modalHandlerLotteryWinningProfile),
    path("modalHandlerLotteryWinning", modalHandlerLotteryWinning),
    path("loadMessagesyHistoryOfProfile", loadMessagesyHistoryOfProfile),
    path("loadMessagesyHistory", loadMessagesyHistory),
    path("deleteProfile", deleteProfile),
    path("deleteMessage", deleteMessage),
    path("closeMessage", closeMessage),
    path("addAdmin", addAdmin),
    path("getAdmins", getAdmins),
    path("removeAdmin", removeAdmin),
    path("addGame", addGame),
    path("getGames", getGames),
    path("removeGame", removeGame),
    path("setCard", setCard),
    path("updateCard", updateCard),
    path("getSettings", getSettings),
    path("updateChannelSettings", updateChannelSettings),
    path("sendMessage", send_message),
    path("sendMessageWithImage", sendMessageWithImage),
    path("sendMessageToWinner", sendMessageToWinner),
    path("sendMessageWithImageToWinner", sendMessageWithImageToWinner),
    path("sendTicket", sendTicket),
    path("setDate", setDate),
    path("selectToWin", selectToWin),
    path("generateExcel", generateExcel),
    path("endLottery", endLottery),
    path('totalUnReadMessagesAndNewPayment', totalUnReadMessagesAndNewPayment, name='totalUnReadMessagesAndNewPayment'),
    path('unReadMessages', unReadMessages, name='unReadMessages'),
    path('getPaymentsDate', getPaymentsDate, name='getPaymentsDate'),
    path('sendToAll', sendToAll, name='sendToAll'),
]