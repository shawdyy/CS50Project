// checking if js is connected
window.addEventListener('load', function(){
  var editable_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4']
  var iframe = document.querySelector('iframe');
  var tagNodeList = [];

  //add clickListener to modal
  var pu = document.querySelector('.modal');
  var editable_content = document.querySelector('.textarea_edit');
  var content_comment = document.querySelector('.textarea_comment');

  //add clickListener to save and close
  var save_button = document.querySelector('#save_changes');
  var close_button = document.querySelector('.close');

  //add clickListener to Button to enter edit mode
  var edit_button = document.querySelector('#editButton');
  var not_edit_button = document.querySelector('#noEditButton');
  edit_button.addEventListener('click', addButtonHandler);
  not_edit_button.addEventListener('click', removeButtonHandler);
  saveAndClose();

  //add global variable for active Event
  var active_element;

  function editTextContent(el){
    pu.style.display = "block";
    let cache = el.innerText;
    active_element = el;
    editable_content.innerHTML = cache.trim();
    editable_content.value = cache.trim();
  }

  function prepareEditTextContent(){
    if (this.childElementCount > 0){
      var check = true;
      for (let i = 0; i < this.childElementCount; i++){
        if (this.children[i].tagName !== "BR" && this.children[i].tagName !== "SPAN" && this.children[i].tagName !== "B"){
          check = false;
        }
      }
      if (check){
        editTextContent(this);
      }
      prepareEditTextContent(this.firstElementChild);
    }
    else if (this.childElementCount === 0){
      editTextContent(this);
    }
    else {

    }
  }

  function addButtonHandler(){
    for (let j = 0; j < editable_tags.length; j++){
      let cacheTagList = iframe.contentDocument.querySelectorAll(editable_tags[j]);
      if (cacheTagList.length > 0){
        tagNodeList.push(cacheTagList);
        for (let i = 0, index = tagNodeList.length-1; i< tagNodeList[index].length; i++){
          tagNodeList[index][i].addEventListener('click', prepareEditTextContent);
        }
      }
      else{
      }
    }
    let divNodeList = [];
    let cacheNodeList = [];
    divNodeList.push(iframe.contentDocument.querySelectorAll('div'));
    for (let i = 0; i < divNodeList; i++){
      if(divNodeList[i].children === 0 && divNodeList[i].innerText.length > 0){
        cacheNodeList.push(divNodeList[i]);
      }
      else{
      }
    }
    if (cacheNodeList.length > 0){
      tagNodeList.push(cacheNodeList);
      for (let i = 0, index = tagNodeList.length-1; i < tagNodeList[index].length; i++){
          tagNodeList[index][i].addEventListener('click', prepareEditTextContent);
      }
    }
    document.querySelector('#nav_heading').style.display = "none";
    console.log(tagNodeList);
  }

  function removeButtonHandler(){
    for(let i=0; i < tagNodeList.length; i++){
      for(let j=0; j < tagNodeList[i].length; j++){
        tagNodeList[i][j].removeEventListener('click', prepareEditTextContent);
      }
    }
    document.querySelector('#nav_heading').style.display = "block";
  }

  //add eventListener for save buttonHandler
  function saveAndClose(){
    save_button.addEventListener('click', function(event){
      event.preventDefault();
      active_element.innerHTML = editable_content.value;
      let json = {
        user: 1,
        project: "test",
        selector: getUniqueSelector(active_element),
        value: editable_content.value,
        comment: content_comment.value
      }
      console.log(json);
      pu.style.display = 'none';
      editable_content.innerHTML = "";
    });
    close_button.addEventListener('click', function(){
      pu.style.display = "none";
      editable_content.innerHTML = "";
    });
  }

  var links = iframe.contentDocument.querySelectorAll('a');
  for (let i = 0; i < links.length; i++){
    links[i].addEventListener('click', function(event){
      event.preventDefault();
    })
  }
}, false)

function getElementSelector(element){
  let selector;
  selector = element.tagName;
  if(element.id){
    selector += "#" + element.id;
  }
  if(element.className){
    selector += "." + element.className.replace(/\s/g, ".")
  }
  return selector;
}

function getElementSiblings(element){
  let nth = 0;
  let siblings = 0;
  let parentNode = element.parentNode;
  for (let i=0; i < parentNode.childElementCount; i++){
    if (parentNode.children[i].tagName === element.tagName){
      siblings++;
      if (parentNode.children[i] === element){
        nth = i+1;
      }
    }
  }
  if (siblings > 1){
    return nth;
  }
  else {
    return -1;
  }
}

function getUniqueSelector(element){
  let cacheArr = [];
  cacheArr.push(getElementSelector(element));
  let activeElement = element;
  while (activeElement.parentNode.tagName !== "BODY"){
    activeElement = activeElement.parentNode;
    let nth = getElementSiblings(activeElement)
    if (nth > 0){
      cacheArr.push(activeElement.tagName + ":nth-child(" + nth + ")");
    }
    else{
      cacheArr.push(activeElement.tagName);
    }
  }
  let uniqueSelector = "";
  for (let i = cacheArr.length -1; i >= 0; i--){
    uniqueSelector += cacheArr[i];
    if (i !== 0){
      uniqueSelector += " > ";
    }
  }
  return uniqueSelector;
}
