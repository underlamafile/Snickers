window.onload = function() {
    setAutoClick()
}

function setAutoClick() {
    setInterval(function() {
        const counter_node = document.getElementById('counter')
        const auto_power_node = document.getElementById('auto_click_power')
        counter_node.innerText = parseInt(counter_node.innerText) + parseInt(auto_power_node.innerText)
    }, 1000)
}

function call_click() {
    const click_node = document.getElementById('click-image')
    click_animation(click_node, 50)

    fetch('mars/call_click/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) return response.json()
        else return Promise.reject(response)
    }).then(data => {
        document.getElementById('counter').innerText = data.main_cycle.coins_count

        if (data.boost) {
            add_boost(data.boost)
        }
    }).catch(err => console.log(err))
}

function update_boost(boost_id) {
    const csrftoken = getCookie('csrftoken')

    fetch('mars/update_boost/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            boost_id: boost_id
        })
    }).then(response => {
        if (response.ok) return response.json()
        else return Promise.reject(response)
    }).then(data => {
        document.getElementById('counter').innerText = data.main_cycle.coins_count
        document.getElementById('click_power').innerText = data.main_cycle.click_power
        document.getElementById('auto_click_power').innerText = data.main_cycle.auto_click_power
        render_boost(data.boost)

    }).catch(err => console.log(err))
}

function add_boost(boost) {
    let boost_holder = document.getElementById('boost-holder')
    const button = document.createElement('button')
    button.setAttribute('class', 'boost')
    if (boost.boost_type == 1)
        button.setAttribute('class', 'boost auto')

    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `update_boost(${boost.id})`)

    button.innerHTML = `
        <p>lvl: <span id="boost_level">${boost.level}</span></p>
        <p>pow: +<span id="boost_power">${boost.power}</span></p>
        <p>buy: <span id="boost_price">${boost.price}</span></p>
    `
    boost_holder.appendChild(button)
}

function render_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price
}

function click_animation(node, time_ms) {
    const css_time = `.0${time_ms}s`
    node.style.cssText = `transition: all ${css_time} linear; transform: scale(0.95);`
    setTimeout(function() {
        node.style.cssText = `transition: all ${css_time} linear; transform: scale(1);`
    }, time_ms)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}