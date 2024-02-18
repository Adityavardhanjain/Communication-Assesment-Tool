function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
  
    tabcontent = document.getElementsByClassName("tab");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    tablinks = document.getElementsByTagName("a");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].classList.remove("active");
    }
  
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
  }
  
  // Open the first tab by default
  document.getElementsByTagName("a")[0].click();