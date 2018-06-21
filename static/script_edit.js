// checking if js is connected
window.addEventListener('load', function(){
  var editable_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4']
  var iframe = document.querySelector('iframe');
  var tagNodeList = [];

  //add clickListener to modal
  var pu = document.querySelector('.modal');
  var editable_content = document.querySelector('.textarea_edit');

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
    console.log(tagNodeList);
  }

  function removeButtonHandler(){
    for(let i=0; i < tagNodeList.length; i++){
      for(let j=0; j < tagNodeList[i].length; j++){
        tagNodeList[i][j].removeEventListener('click', prepareEditTextContent);
      }
    }
  }

  //add eventListener for save buttonHandler
  function saveAndClose(){
    save_button.addEventListener('click', function(event){
      event.preventDefault();
      active_element.innerHTML = editable_content.value;
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
