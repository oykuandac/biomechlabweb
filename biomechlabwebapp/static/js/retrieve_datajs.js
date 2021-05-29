function getOption() { 

  var resultSet = validate();
  var outputs = []
  for(var i=0;i<resultSet.length;i++){
      if(resultSet[i]!="age" && resultSet[i]!="bmi"){
        var name = "#"+resultSet[i];
        selectElement =  document.querySelector(name);      
        output = selectElement.value; 
        document.querySelector('.output').textContent = output;
        outputs.push(output.toUpperCase());
      }
    }
    return outputs;
}

function getAge(str){
    var flag = false;
    if(document.getElementById("age").selectedIndex <=0 )
    {
      flag = true;
    }else{
      selectElement =  document.querySelector("#age");      
      output = selectElement.value; 
      document.querySelector('.output').textContent = output;
      firstNum = parseInt(output.substring(0,2));
      secondNum = parseInt(output.substring(3,5));
      for(var i=firstNum; i<secondNum+1;i++){
        if(str.includes("A"+i.toString())){
            flag = true;
        }
      }
    }

    return flag;
}

function getBmi(str){
  var flag = false;
  if(document.getElementById("bmi").selectedIndex <=0)
  {
    flag = true;
  }else{
    selectElement =  document.querySelector("#bmi");      
    output = selectElement.value; 
    document.querySelector('.output').textContent = output;
    if(output=="<18"){
      if(str.includes("BLT18")){
       
          flag = true;
      }
    }
    else if(output==">40"){
      if(str.includes("BGT40")){
          flag = true;
      }
    }else{
      firstNum = parseFloat(output.substring(0,2));
      secondNum = parseFloat(output.substring(3,7)) +0.1;
      for(var i=firstNum; i<secondNum+1;i++){
        if(str.includes("B"+i.toString())){
                
            flag = true;
        }
      }
    }
  }
 return flag;
}

function getAllFiles(){
  var out;
  var outputs = getOption();
  var files = [];
   var table = document.getElementById('table1');
    for (var r = 0, n = table.rows.length; r < n; r++) {
      for (var c = 0, m = table.rows[r].cells.length; c < m; c++) {
        current = table.rows[r].cells[c].innerHTML;
        var hasEvery = checkContains(current, outputs);
        var hasAge = getAge(current);
        var hasBmi = getBmi(current);
        if(hasEvery && hasAge && hasBmi)
        {
           out = table.rows[r].cells[c].innerHTML; 
           files.push(out);  
        }
      
      }
    }
   return files;
}
function checkContains(str, arr){
  
  return arr.every(item => str.includes(item));
}

function validate()
 {
   var activite = document.getElementById("activity");
   var age = document.getElementById("age");
   var gender = document.getElementById("gender");
   var bmi = document.getElementById("bmi");
   var resultSet = [];
   if(!activite.selectedIndex <=0)
    {
      resultSet.push("activity");
    }
    if(!age.selectedIndex <=0)
    {
      resultSet.push("age");
    }
    if(!gender.selectedIndex <=0)
    {
      resultSet.push("gender");
    }
    if(!bmi.selectedIndex <=0)
    {
      resultSet.push("bmi");
    }
    return resultSet;
 }

var current_page = 1;
var records_per_page = 15;


function prevPage()
{
    if (current_page > 1) {
        current_page--;
        changePage(current_page);
    }
}

function nextPage()
{
    if (current_page < numPages()) {
        current_page++;
        changePage(current_page);
    }
}
    
function changePage(page)
{
    var btn_next = document.getElementById("btn_next");
    var btn_prev = document.getElementById("btn_prev");
    var listing_table = document.getElementById("listingTable");
    var page_span = document.getElementById("page");
    // Validate page
    if (page < 1) page = 1;
    if (page > numPages()) page = numPages();

    listing_table.innerHTML = "";

    for (var i = (page-1) * records_per_page; i < (page * records_per_page) && i < getAllFiles().length; i++) {
      if(getAllFiles()[(i)] != undefined){
        
        listing_table.innerHTML += getAllFiles()[(i)] + "<br>";
      }
    }

    page_span.innerHTML = page + "/" + numPages();

    if (page == 1) {
        btn_prev.style.visibility = "hidden";
    } else {
        btn_prev.style.visibility = "visible";
    }

    if (page == numPages()) {
        btn_next.style.visibility = "hidden";
    } else {
        btn_next.style.visibility = "visible";
    }
}

function numPages()
{
    return Math.ceil(getAllFiles().length / records_per_page);
}
