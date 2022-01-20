# Flask-MongoDB App: "cBay"

## Description:

This web app relies upon a MongoDB database, Pymongo and Flask. The web app connects buyers and sellers of various products. It takes information from sellers such as `name`, `email`, `item name`, `condition`, `category`, `price`, `description` and `shipping` and saves them into the MongoDB collection `market`. Any updating and deleting of the listings will also be through the MongoDB `market` collection. The categories are predetermined and are offered in a list when the seller goes to create a new listing. When the user is creating a listing, they will be asked to provide a password for the specific listing (and prompted to save that password in a secure place). In this way, if the user wants to edit or delete the product, it would first redirect the user to another page to verify whether the user is the one who posted the listing, before proceeding. Upon receiving an incorrect password, the user is redirected to an "Error" page, before being returned to the main "Read" page. If an interested party wants to contact the seller of a particular product, there is a convenient `Email Seller` button which will open the Mail app automatically.

This web app also allows the users to leave comments on a specific listing. The item name is a link, which will redirect the user to the item page with comments on the bottom of the page, in order of most recent. Users can edit, post, and delete comments and the information is stored in the `comments` collection in MongoDB. 

Lastly, there is a filter system that allows the user to filter by condition (of the item), Item Category, Price, and whether Shipping is included. The home page also includes a few handy links for when users are looking for items under a particular price.
 
## Links

Here is the link for our web app, a tentatively (jokingly) named [cBay](https://i6.cims.nyu.edu/~yx2017/web-app-charlie-solo/flask.cgi/).

## Collaborators

Charlie Xiang, yx2017, [Github](https://github.com/xiang-charlie)  
Rachel Qiu, rq374, [Github](https://github.com/Rachelq7)
