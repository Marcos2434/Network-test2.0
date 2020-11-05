document.addEventListener('DOMContentLoaded', () => {
    
    like_logic()

    edit()
     
})

function edit() {
    const editButton = document.querySelectorAll('#editButton')

    editButton.forEach(btn => {

        btn.onclick = (event) => {

            event.preventDefault()
            btn.disabled = true

            post =  btn.parentNode.parentNode    
            post_content = post.querySelector('#post_content')
            post_to_edit = event.target.dataset.post_id

            post_content.style.display = 'none'

            //create form 
            const form = document.createElement('form')

            // event listener  
            form.onsubmit = (event) => {
                event.preventDefault()

                //xml POST request 
                const xmlrequest = new XMLHttpRequest()
                xmlrequest.open('POST', '/edit', true)
                const csrftoken = getCookie('csrftoken')
                xmlrequest.setRequestHeader('X-CSRFToken', csrftoken)
                
                //data to send 
                xmlrequest.send(
                    JSON.stringify({
                        post_id : post_to_edit,
                        content : textarea.value
                    })
                )

                //remove the form 
                btn.innerHTML = 'Edit'
                post_content.style.display = 'block'
                post_content.innerHTML = textarea.value
                form.remove()

                //reactivate button
                btn.disabled = false
            }
            
            //create element textarea to put in form
            const textarea = document.createElement('textarea')
            textarea.classList.add('form-control')
            textarea.value = post_content.innerHTML // or maybe get from fetch?
            textarea.id = 'editPost'

            const submit = document.createElement('input')
            submit.classList.add('btn-sm') 
            submit.classList.add('btn-info')
            submit.type = 'submit' 
            submit.value = 'Save edit' 

            form.append(textarea)
            form.append(document.createElement('br'))
            form.append(submit)
            event.target.append(form)
            
            btn.parentNode.appendChild(form)
            

            /*

            // hide current post content and change button
            if (btn.innerHTML == 'Save') {
                btn.innerHTML = 'Edit'
                post_content.style.display = 'block'
                post.querySelector('#editPost').remove()
                
                return

            } 
            
            btn.innerHTML = 'Save'
            post_content.style.display = 'none'
            
            //create form 
            const form = document.createElement('form')

            form.onsubmit = (event) => {
                /*event.preventDefault()

                const request = new XMLHttpRequest()


                request.open('POST', '/edit_post', true)
                const csrftoken = getCookie('csrftoken')
                request.setRequestHeader('X-CSRFToken', csrftoken)


                data = {
                    post_id: cardBody.dataset.post_id,
                    edited_text: textarea.value,
                };

                request.send(JSON.stringify(data))*/
            }
    })
}

// https://docs.djangoproject.com/en/dev/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function like_logic() {
    const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];
    const post_like = document.querySelectorAll('#post_like');
    post_like.forEach(post => {
        fetch('/liked')
        .then(response => response.json())
        .then(data => { 
            //console.log(`${data.user_liked} : ${post.dataset.post_id}`)
            
            user_liked = data['user_liked'];
            list = []
            for (const i in user_liked) { 
                list.push(user_liked[i]);
            }

            for (const id in list) {
                //console.log(`${list[id]} : ${post.dataset.post_id}`)
                if (post.dataset.post_id == list[id]) {
                    post.classList.add('fas');
                } else {
                    post.classList.add('far');
                }
            }

            for (const likes in data['likes_per_post']) {
                if (post.dataset.post_id == likes) {
                    post.innerHTML = ` ${data['likes_per_post'][likes]}`;
                }   
            }
        })

        post.onclick = (event) => {
            //reset animation
            event.target.classList.remove('grow');
            
            try {
                user_liked = document.querySelector('#user_id').innerHTML
            } catch(error) {
                console.log(error)
            }
            var data = {
                user_liked : user_liked,
                post_liked : event.target.dataset.post_id
            };

            fetch('/liked', {
                method:'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body : JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data['post_liked']) {
                    event.target.classList.remove('far');
                    event.target.classList.add('fas');

                    event.target.classList.add('grow');
                    event.target.innerHTML = ` ${data['like_count']}`
                } else {
                    event.target.classList.remove('fas');
                    event.target.classList.add('far');

                    event.target.classList.add('grow');
                    event.target.innerHTML = ` ${data['like_count']}`
                }
            });
        }
    })
}

// Get the user
/*
fetch('/get_user')
.then(response => response.json)
.then(user => user)
*/