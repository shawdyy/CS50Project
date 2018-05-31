// checking if js is connected
window.addEventListener('load', function(){
  var editable_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4']
  var iframe = document.querySelector('iframe');
  var tagNodeList = []

  //add clickListener to Button to enter edit mode
  var edit_button = document.querySelector('#trigger_edit');
  edit_button.addEventListener('click', buttonHandler);

  //add clickListener to modal
  var pu = document.querySelector('.modal');
  var editable_content = document.querySelector('.textarea_edit');

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
        if (this.children[i].tagName !== "BR"){
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

  function buttonHandler(){
    for (let j = 0; j < editable_tags.length; j++){
      tagNodeList.push(iframe.contentDocument.querySelectorAll(editable_tags[j]));
      for (let i = 0; i< tagNodeList[j].length; i++){
        tagNodeList[j][i].addEventListener('click', prepareEditTextContent);
      }
    }
  }

  //add eventListener for save buttonHandler
  var save_button = document.querySelector('#save_changes');
  save_button.addEventListener('click', function(event){
    event.preventDefault();
    active_element.innerHTML = editable_content.value;
    pu.style.display = 'none';
    editable_content.innerHTML = "";
  })

  var close_button = document.querySelector('.close');
  close_button.addEventListener('click', function(){
    pu.style.display = "none";
    editable_content.innerHTML = "";
  })

  var links = iframe.contentDocument.querySelectorAll('a');
  for (let i = 0; i < links.length; i++){
    links[i].addEventListener('click', function(event){
      event.preventDefault();
    })
  }
}, false)
