window.addEventListener('load', function(){
  let p_elements = document.querySelectorAll('.p_element_container');

  for(let i = 0; i < p_elements.length; i++){
    let that = p_elements[i];
    if (that.querySelector('a > div:nth-child(1)').classList.value == "p_new_element"){
      that.addEventListener('mouseenter', function(){
        this.querySelector('a > div:nth-child(2)').style.color = "#EFEFEF"
        this.querySelector('a > div:nth-child(1)').style.background = "#555";
        this.querySelector('a > div:nth-child(1) > span').style.color = "white";
      });
      that.addEventListener('mouseleave', function(){
        this.querySelector('a > div:nth-child(2)').removeAttribute('style');
        this.querySelector('a > div:nth-child(1)').removeAttribute('style');
        this.querySelector('a > div:nth-child(1) > span').removeAttribute('style');
      });
    }
    else{
      that.addEventListener('mouseenter', function(){
        this.querySelector('a > div:nth-child(1) > img').style.opacity = "0.6"
        this.querySelector('a > div:nth-child(1)').style.background = "#555";
        this.querySelector('.p_description').style.color = "white";
      });
      that.addEventListener('mouseleave', function(){
        this.querySelector('a > div:nth-child(1) > img').removeAttribute('style');
        this.querySelector('a > div:nth-child(1)').removeAttribute('style');
        this.querySelector('.p_description').removeAttribute('style');
      });
    }
  }
});
