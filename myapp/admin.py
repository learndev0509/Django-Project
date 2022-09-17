from django.contrib import admin
from .models import User,Product,Contact,Wishlist,Cart,Transaction,Subscribe,Reviews
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Transaction)
admin.site.register(Subscribe)
admin.site.register(Reviews)