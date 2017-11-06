/**
 * file for orders
 * 
 */
window.orders = {

  /**
   * deletes something from the cart
   */

  deleteAction: (e) => {
    e.preventDefault();
    let elem = e.target;
    mbox.confirm('¿Seguro que desea eliminar esto del carrito?', (yes) => {
      const formData = new FormData();
      const id       = elem.dataset.lineitemid;
      formData.append("line_item_id", id);

      // let's go.
      //
      fetch(removeItemUrl,
      {
          method: "POST",
          credentials: "same-origin",
          headers: {
              "X-CSRFToken": Cookies.get('csrftoken'),
              "Accept": "application/json",
          },
          body: formData
      }).then((response) => {
        return response.json();
      }).then((data) => {
          console.log(data);
        if(data.RESULT == "OK"){
            document.querySelector('#i' + id).style = "display: none;";
            /*
            var lis     = document.querySelectorAll('tbody tr');
            var isEmpty = true;
            for(let i = 0; i < lis.length; i++) {
                isEmpty = isEmpty && lis[i].style.length > 0;
            }
            if(isEmpty) {
                document.querySelector('#continue').style = "display: none;";
                document.querySelector('tbody').innerHTML = // ↓
                "<tr><td></td><td>No hay productos en el carrito.</td></tr>";
            }*/
        }
      }).catch(function(error) {
        //alert('Lo sentimos. Algo pasó. :(');
         console.error(error);
      });
    }).bind(this);
  },

  changeAction: (e) => {
    const quantity = parseFloat(e.target.value);
    const price    = parseFloat(e.target.dataset.price);
    const total    = quantity * price;

    const elemTotal = document.getElementById('total' + e.target.dataset.id);

    if(isNaN(total)) {
        elemTotal.innerHTML = "0.00";
    } else {
        // TODO: Fix this
        elemTotal.innerHTML = total.toLocaleString() + ".00";
    }
  },

  selectAction: (e) => {
    if(option.value === "no-options") {
      return;
    }
    const option       = e.target.selectedOptions[0];
    const quantityElem = e.target.parentElement.parentElement.
                         querySelector('.quantity');
    quantityElem.dataset.price = option.value ? option.dataset.price : 0;

    e.target.parentElement.parentElement. // ↓
    querySelector('td:nth-child(3) span'). // ↓ YISUSCRAIST
    innerHTML = option.dataset.priceprint;

    const event = new Event('input', {
        'bubbles':    true,
        'cancelable': true
    });
    quantityElem.dispatchEvent(event);
  }
};

document.querySelector('#update_cart').addEventListener("click", function(e){
    e.preventDefault();
    var form = document.querySelector("#items");
    var form_data =  new FormData(form);
    fetch(form.action,
      {
          method: "POST",
          credentials: "same-origin",
          headers: {
              "X-CSRFToken": Cookies.get('csrftoken'),
          },
          body: form_data
      }).then((response) => {
        location.reload();
    });
}, false);

(function ($) {
  if (typeof editOrder === 'undefined') {
    return;
  }

  const buttons = document.querySelectorAll('.delete');
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click",    window.orders.deleteAction, false);
  }

  const quantities = document.querySelectorAll('.quantity');
  for (let i = 0; i < quantities.length; i++) {
    quantities[i].addEventListener("input", window.orders.changeAction, false);
  }
  
  const selects = document.querySelectorAll('.type');

  for (let i = 0; i < selects.length; i++) {
    selects[i].addEventListener("change", changeSelection, false);
    
    var event = new Event('change', {
            'bubbles':    true,
            'cancelable': true
    });

    selects[i].dispatchEvent(event);
  }

})(jQuery);



