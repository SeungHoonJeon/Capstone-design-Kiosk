const categoryBtns = document.querySelectorAll('.category-btn');
const menuItems = document.querySelectorAll('.menu-item');

categoryBtns.forEach(btn => { 
  btn.addEventListener('click', () => {
    const category = btn.dataset.category; // 양식, 중식 ,한식
    menuItems.forEach(item => { //
      if (item.classList.contains(category)) { //아이템들이 양식, 중식, 한식 중 각가 포함된 것을 block 단위로 만듦.
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
    });
  });
});
const cartItems = [];

//1. 이벤트 발생시 실행
function addToCart(name, price) {
  let item = cartItems.find(item => item.name === name);
  if (item) { //기존에 담긴 아이템 추가시 수량 증가
    item.quantity++; 
    updateCartItem(item);
  } else {

    //아이템 추가
    cartItems.push({ name, price, quantity: 1 });
    const cart = document.getElementById('cart-items'); // <!--선택메뉴--> dom 객체 생성.
    const li = document.createElement('li'); // li태그에 추가.
    li.innerHTML = `${name} - ${price}원 x <span>${1}</span>개
                    <button type="button" onclick="increaseCartItem('${name}')">+</button>
                    <button type="button" onclick="decreaseCartItem('${name}')">-</button>
                    <button type="button" onclick="removeCartItem('${name}')">삭제</button>`;  //li태그에 음식명, 갯수, 가격 버튼 추가
    li.setAttribute('id', name); // li태그에 id 음식명 설정
    cart.appendChild(li); // ul태그 cart-items에 위 li내용 자식으로 추가
    updateTotalPrice();
  }
}

function updateCartItem(item) {
  const cartItem = document.getElementById(item.name);
  cartItem.querySelector('span').textContent = item.quantity;
  updateTotalPrice();
}

function increaseCartItem(name) {
  const item = cartItems.find(item => item.name === name); //해당 아이템을 찾아서 수량 증가
  item.quantity++;
  updateCartItem(item);
}

function decreaseCartItem(name) {
  const item = cartItems.find(item => item.name === name); // 수량 감소. 혹은 삭제
  if (item.quantity > 1) {
    item.quantity--;
    updateCartItem(item);
  } else {
    removeCartItem(name);
  }
}

function removeCartItem(name) {
  const itemIndex = cartItems.findIndex(item => item.name === name);
  if (itemIndex !== -1) {
    cartItems.splice(itemIndex, 1);
    const cartItem = document.getElementById(name);
    cartItem.remove();
    updateTotalPrice();
  }
}


function updateTotalPrice() {
  const totalPrice = document.getElementById('total-price');
  const price = cartItems.reduce((total, item) => total + item.price * item.quantity, 0); //추가된 item 반복문을 돌려서 가격 * 수량 해서 total 넣어서 다 더함.
  totalPrice.textContent = `총 가격: ${price}원`; //총 가격 출력.
}

function showKiosk(category) {
  const kiosk = document.getElementById('kiosk');
  kiosk.style.display = 'block';
  const categoryHeading = document.getElementById('category');
  categoryHeading.textContent = `${category} 메뉴`;
}