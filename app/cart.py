from .models import ImageProduct


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})
        self.quantity_cart = self.session.get('quantity_cart', 0)
        

    def add(self, product, quantity=1):
        product_id = str(product.id)
        
        # Obtener la primera imagen asociada
        images = ImageProduct.objects.filter(product_id=product.id)        
        first_image = images.first()        
        image_url = ''
        
        if first_image.image.url:
            image_url = first_image.image.url
    
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image': image_url,
                'total': product.price * quantity
            }
            self.quantity_cart = self.quantity_cart + quantity
        self.save()

    def remove(self, product):
        cart = self.session['cart']
        quantity_cart = self.session['quantity_cart']
        product_id = str(product.id)
        
        if product_id in self.cart:
            self.session['quantity_cart'] = quantity_cart - cart[product_id]['quantity']
            del self.cart[product_id]

    def save(self):
        self.session['cart'] = self.cart
        self.session['quantity_cart'] += 1
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session['quantity_cart'] = 0
        self.session.modified = True

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def items(self):
        return self.cart.values()
