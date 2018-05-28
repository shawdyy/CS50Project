// checking if js is connected
window.addEventListener('load', function(){
  var editable_tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4']
  var iframe = document.querySelector('iframe');
  var tagNodeList = []

  //add clickListener to Button to enter edit mode
  var edit_button = document.querySelector('#trigger_edit');
  edit_button.addEventListener('click', buttonHandler);

  function buttonHandler(){
    for (let j = 0; j < editable_tags.length; j++){
      tagNodeList.push(iframe.contentDocument.querySelectorAll(editable_tags[j]));
      for (let i = 0; i< tagNodeList[j].length; i++){
        tagNodeList[j][i].addEventListener('click', function(){
          if (!this.classList.contains('selected')){
            this.classList.add('selected');
          } else {
            this.classList.remove('selected');
          }
        });
      }
    }
  }

  var popup_button = document.querySelector('#trigger_popup');
  var pu = document.querySelector('.modal');
  popup_button.addEventListener('click', function(){
    pu.style.display = "block";
  })

  var close_button = document.querySelector('.close');
  close_button.addEventListener('click', function(){
    pu.style.display = "none";
  })

  var links = iframe.contentDocument.querySelectorAll('a');
  for (let i = 0; i < links.length; i++){
    links[i].addEventListener('click', function(event){
      event.preventDefault();
    })
  }
}, false)
