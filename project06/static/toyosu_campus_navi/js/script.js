function openModal() {
  document.getElementById("modal").classList.add("active");
}

function closeModal() {
  document.getElementById("modal").classList.remove("active");
}

//第一引数のメニューを非表示にして、第二引数のメニューを表示する
function openMenu(currentMenuId,targetMenuId){
  document.getElementById(currentMenuId).style.display="none";
  document.getElementById(targetMenuId).style.display="contents";
}