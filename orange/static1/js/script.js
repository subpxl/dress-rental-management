
function addToTable(name, tag, price) {
  productTable = document.getElementById("tableBody");
  var row = productTable.insertRow(0);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  cell1.innerHTML = name;
  cell2.innerHTML = tag;
  cell3.innerHTML = price;
}

function makeTable(tag) {
    productList = [];
    fetch('/product/search',

        {
  method: 'POST',
  headers: {
    Accept: 'application.json',
    'Content-Type': 'application/json'
  },

          Body: JSON.stringify(tag),

})
    .then((response) => response.json())
    .then((data) => {
      data.forEach((product) => {
        productList.push({
          name: product.fields.name,
          tag: product.fields.tag,
          price: product.fields.price,
        });

        addToTable(
            product.fields.name,
            product.fields.tag,
            product.fields.price,)
      });
    })


}



// makeTable()

productSearchForm = document.getElementById('productSearchForm').addEventListener('click',
    function(event){
  event.preventDefault()

      form = event.currentTarget
      url = form.action
      tagInput = document.getElementById("tag").value;
      console.log(tagInput)

      makeTable(tagInput)


    }
)

