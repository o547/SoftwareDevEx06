//モーダルを活性にする
function openModal() {
  document.getElementById("modal").classList.add("active");
}

//モーダルを非活性にする
function closeModal() {
  document.getElementById("modal").classList.remove("active");
}

//第一引数のメニューを非表示にして、第二引数のメニューを表示する
function toggleMenu(currentMenuId, targetMenuId, displayMethod) {
  document.getElementById(currentMenuId).style.display = "none";
  document.getElementById(targetMenuId).style.display = displayMethod;
}

