console.log("connected");

function buttonHandler(){
  var iframe = document.querySelector('iframe');
  console.log(iframe);
  var cache = iframe.contentDocument.querySelectorAll('p');
  console.log(cache);
  cache[1].addEventListener('click', console.log("clicked"));
}

var edit_button = document.querySelector('#trigger_edit');
edit_button.addEventListener('click', buttonHandler);

/*
var editing_mode = false;
var editable_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p'];

function buttonHandler(event){
  if (editing_mode){
    editing_mode = false;
    console.log(event);
  }
  else{
    var iframe = document.querySelector('iframe');
    for(let i = 0; i < editable_tags.length; i++){
      let cache = iframe.contentDocument.querySelectorAll(editable_tags[i]);
      cache.addEventListener('click', clickHandler);
    }
    editing_mode = true;
  }
  console.log('lol click');
}

var edit_button = document.querySelector('#trigger_edit');
edit_button.addEventListener('click', buttonHandler);


function clickHandler(event){
  if (event.classList.contains('selected')){
    event.classList.remove('selected');
  }
  else{
    event.classList.add('selected');
  }
  console.log(event.srcElement);
}*/
