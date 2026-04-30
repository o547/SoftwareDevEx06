function openModal() {
  document.getElementById("modal").classList.add("active");
}

function closeModal() {
  document.getElementById("modal").classList.remove("active");
}

function openMenu(currentMenuId,targetMenuId){
  document.getElementById(currentMenuId).style.display="none";
  document.getElementById(targetMenuId).style.display="contents";
}