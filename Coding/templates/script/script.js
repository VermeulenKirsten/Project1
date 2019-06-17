// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');

const varip = window.location.hostname;
const IP = `${varip}:5000`;
const socketio = io.connect(IP);

let deliveries = [0, 0, 0, 0, 0, 0, 0];
let collections = [0, 0, 0, 0, 0, 0, 0];
let labels = ['', '', '', '', '', '', ''];

let time = [];
let timelabels = [];

//#region ***********  DOM references ***********

//#endregion

//#region ***********  Callback - HTML Generation (After select) ***********
// show________

const show_dropdown = function() {
  if (document.querySelector('.js-menu').classList.contains('c-dropdown-show')) {
    document.querySelector('.js-menu').classList.remove('c-dropdown-show');
  } else {
    document.querySelector('.js-menu').classList.add('c-dropdown-show');
  }
};

const show_bar_graph = function(data) {
  let date = new Date();
  let teller = 0;

  for (teller = 6; teller >= 0; teller--) {
    for (let item of data) {
      if (date.getDate() - 6 + teller == item['day'] && item['actie'] == 'In use') {
        deliveries[teller] += 1;
        if (labels.includes(item['date']) == false) {
          labels[teller] = item['date'];
        }
      }
      if (date.getDate() - 6 + teller == item['day'] && item['actie'] == 'Empty') {
        collections[teller] += 1;
      }
    }
  }

  let ctx = document.getElementById('bars').getContext('2d');

  let chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Deliveries',
          backgroundColor: 'rgb(60, 224, 236)',
          pointBackgroundColor: 'rgb(255, 255, 255)',
          data: deliveries,
          pointRadius: 3,
          pointBorderWidth: 0.5,
          borderWidth: 0.5
        },
        {
          label: 'Collections',
          backgroundColor: 'rgb(255, 202, 121)',
          pointBackgroundColor: 'rgb(255, 255, 255)',
          data: collections,
          pointRadius: 3,
          pointBorderWidth: 0.5,
          borderWidth: 0.5
        }
      ]
    },

    // Configuration options go here
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          boxWidth: 15
        }
      },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true
            }
          }
        ]
      }
    }
  });
};

const show_donut_graph = function(data) {
  console.log(data);
  let ctx = document.getElementById('donut').getContext('2d');
  let index = 0;
  let background_color = [];
  let random_rgb;
  let teller = 0;
  for (let item of data) {
    console.log(item);
    if (timelabels.includes(item['hour'] + 'u') == false) {
      timelabels.push(item['hour'] + 'u');
      time.push(1);
    } else {
      index = timelabels.indexOf(item['hour'] + 'u');
      time[index] += 1;
    }
  }

  console.log(time.length);

  if (time.length <= 3) {
    background_color = ['rgb(60, 224, 236)', 'rgb(255, 202, 121)', 'rgb(125, 115, 195)'];
  } else {
    background_color = ['rgb(60, 224, 236)', 'rgb(255, 202, 121)', 'rgb(125, 115, 195)'];

    for (teller = 3; teller < time.length; teller++) {
      random_rgb = 'rgb(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ')';

      background_color.push(random_rgb);
    }
  }

  let chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'doughnut',

    // The data for our dataset
    data: {
      labels: timelabels,
      datasets: [
        {
          label: 'Deliveries',
          backgroundColor: background_color,
          pointBackgroundColor: 'rgb(255, 255, 255)',
          data: time,
          pointRadius: 3,
          pointBorderWidth: 0.5,
          borderWidth: 0.5
        }
      ]
    },

    // Configuration options go here
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: true,
        position: 'right',
        labels: {
          boxWidth: 15
        }
      }
    }
  });
};

const show_lockers = function(data) {
  let html = '';
  let date = '';
  let hour = '';

  for (let item of data) {
    if (item['status'] == 0) {
      html += `<div class="o-layout__item u-1-of-2-bp4">
      <div class="c-widget u-box-shadow-bottom">
        <div class="c-widget__header">
          <h6>Locker ${item['lockerID']}</h6>
        </div>

        <hr class="u-widget-line" />

        <div class="c-widget__content">
          <div class="o-layout">
            <div class="o-layout__item u-2-of-3">
              <p class="">Status:</p>
            </div>
            <div class="o-layout__item u-1-of-3 u-text-align-right">
              <p class="c-widget__text">Empty</p>
            </div>
          </div>

          <a class="c-link-cta u-box-shadow-bottom js-open-locker" data-locker="${item['lockerID']}" href="#">Open</a>
        </div>
      </div>
    </div>`;
    } else if (item['status'] == 1) {
      date = item['laatst_geopend'].split(' ');
      hour = date[4].split(':');

      html += `<div class="o-layout__item u-1-of-2-bp4">
      <div class="c-widget u-box-shadow-bottom">
        <div class="c-widget__header">
          <h6>Locker ${item['lockerID']}</h6>
        </div>
        <hr class="u-widget-line" />
        <div class="c-widget__content">
          <div class="o-layout">
            <div class="o-layout__item u-2-of-3">
              <p class="c-widget__text">Status:</p>
            </div>
            <div class="o-layout__item u-1-of-3 u-text-align-right">
              <p class="c-widget__text">In use</p>
            </div>
          </div>

          <div class="o-layout">
            <div class="o-layout__item u-2-of-3">
              <p>Date of commissioning:</p>
            </div>
            <div class="o-layout__item u-1-of-3 u-text-align-right">
              <p>${date[0]} ${date[1]} ${date[2]} ${date[3]} ${hour[0]}u${hour[1]}</p>
            </div>
          </div>

          <p class="c-widget__title">Owner:</p>

          <div class="o-layout">
            <div class="o-layout__item u-1-of-3">
              <p class="c-widget__text">Name:</p>
            </div>
            <div class="o-layout__item u-2-of-3 u-text-align-right">
              <p class="c-widget__text">${item['voornaam']} ${item['achternaam']}</p>
            </div>
          </div>

          <div class="o-layout">
            <div class="o-layout__item u-1-of-3">
              <p class="c-widget__text">Address:</p>
            </div>
            <div class="o-layout__item u-2-of-3 u-text-align-right">
              <p class="c-widget__text">${item['straat']} ${item['huisnummer']}</p>
              <p class="c-widget__text">${item['postcode']} ${item['gemeente']}</p>
            </div>
          </div>

          <div class="o-layout">
            <div class="o-layout__item u-1-of-3-bp1">
              <p class="c-widget__text">E-mail:</p>
            </div>
            <div class="o-layout__item u-2-of-3-bp1 u-text-align-right u-text-align-left-bp1">
              <p>${item['email']}</p>
            </div>
          </div>

          <a class="c-link-cta u-box-shadow-bottom js-open-locker" data-locker="${item['lockerID']}" href="#">Open</a>
        </div>
      </div>
    </div>`;
    }
  }

  document.querySelector('.js-locker-html').innerHTML = html;
  listen_to_open();
};

const show_admin_history = function(data) {
  let date = '';
  let hour = '';

  let html = `<div class="c-widget__header">
  <h6>Admin History</h6>
</div>
<hr class="u-widget-line" /><div class="c-widget__content">
  <div class="o-layout c-widget__title">
    <div class="o-layout__item u-1-of-3">
      <p>Date</p>
    </div>
    <div class="o-layout__item u-1-of-3">
      <p>Hour</p>
    </div>
    <div class="o-layout__item u-1-of-3 u-text-align-right">
      <p>Badge</p>
    </div>
  </div>`;

  for (let item of data) {
    date = item['tijd_van_actie'].split(' ');
    hour = date[4].split(':');

    html += `<div class="o-layout c-widget__text">
    <div class="o-layout__item u-1-of-3">
      <p class="c-widget__text">${date[1]} ${date[2]}</p>
    </div>
    <div class="o-layout__item u-1-of-3">
      <p class="c-widget__text">${hour[0]}u${hour[1]}</p>
    </div>
    <div class="o-layout__item u-1-of-3 u-text-align-right">
      <p class="c-widget__text">${item['actie']}</p>
    </div>
  </div>`;
  }

  html += `</div>`;

  document.querySelector('.js-admin-history').innerHTML = html;
};

const show_user_history = function(data) {
  let date = '';
  let hour = '';

  html = `<div class="c-widget__header">
  <h6>User History</h6>
</div>
<hr class="u-widget-line" />
<div class="c-widget__content">
  <div class="o-layout c-widget__title">
    <div class="o-layout__item u-1-of-4">
      <p>Date</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-center">
      <p>Hour</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-center">
      <p>locker</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-right">
      <p>Action</p>
    </div>
  </div>`;

  for (let item of data) {
    date = item['tijd_van_actie'].split(' ');
    hour = date[4].split(':');

    html += `<div class="o-layout c-widget__text">
    <div class="o-layout__item u-1-of-4">
      <p class="c-widget__text">${date[1]} ${date[2]}</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-center">
      <p class="c-widget__text">${hour[0]}u${hour[1]}</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-center">
      <p class="c-widget__text">locker ${item['lockerID']}</p>
    </div>
    <div class="o-layout__item u-1-of-4 u-text-align-right">
      <p class="c-widget__text">${item['actie']}</p>
    </div>
  </div>`;
  }

  html += `</div>`;

  document.querySelector('.js-user-history').innerHTML = html;
};

const show_dashboard_lockers = function(data) {
  let html = '';
  let status = '';

  console.log(data);

  for (let item of data) {
    if (item['status'] == 0) {
      status = 'Empty';
    } else if (item['status'] == 1) {
      status = 'In use';
    }

    html += `<div class="o-layout">
    <div class="o-layout__item u-1-of-2">
      <p class="c-widget__title">Locker ${item['lockerID']}</p>
    </div>
    <div class="o-layout__item u-1-of-2 u-text-align-right">
      <a class="c-link-cta u-box-shadow-bottom js-open-locker" data-locker="${item['lockerID']}" href="#">Open</a>
    </div>
  </div>
  <p>${status}</p>`;
  }

  document.querySelector('.js-dashboard-lockers').innerHTML = html;
  listen_to_open();
};

const show_dashboard_recent_events = function(data) {
  let date = '';
  let hour = '';
  let actie = '';

  html = `<div class="o-layout c-widget__title">
  <div class="o-layout__item u-1-of-3">
    <p>Date</p>
  </div>
  <div class="o-layout__item u-1-of-3 u-text-align-center">
    <p>Hour</p>
  </div>
  <div class="o-layout__item u-1-of-3 u-text-align-right">
    <p>Action</p>
  </div>
</div>`;

  for (let item of data) {
    date = item['tijd_van_actie'].split(' ');
    hour = date[4].split(':');

    if (item['lockerID'] == null) {
      actie = 'Badge';
    } else {
      actie = item['actie'];
    }

    html += `<div class="o-layout">
    <div class="o-layout__item u-1-of-3">
      <p class="c-widget__text">${date[1]} ${date[2]}</p>
    </div>
    <div class="o-layout__item u-1-of-3 u-text-align-center">
      <p class="c-widget__text">${hour[0]}u${hour[1]}</p>
    </div>
    <div class="o-layout__item u-1-of-3 u-text-align-right">
      <p class="c-widget__text">${actie}</p>
    </div>
  </div>`;
  }

  document.querySelector('.js-dashboard-recent-events').innerHTML = html;
};

//#endregion

//#region ***********  Callback - (After update/delete/insert) ***********
// callback______

const callback_login = function(data) {
  console.log(data);
  if (data['length'] > 0) {
    localStorage.setItem('wachtwoord', data[0]['wachtwoord']);
    window.location.replace('dashboard.html');
  }
};

const callback_open = function(locker) {
  socketio.emit('open_locker', locker);
};

//#endregion
//#region ***********  Data Access ***********
// get_______

const get_lockers = function() {
  handleData('http://' + IP + '/lockers', show_lockers);
};

const get_history = function() {
  handleData('http://' + IP + '/admin_history', show_admin_history);
  handleData('http://' + IP + '/user_history', show_user_history);
};

const get_dashboard = function() {
  handleData('http://' + IP + '/dashboard_bar_graph', show_bar_graph);
  handleData('http://' + IP + '/dashboard_donut_graph', show_donut_graph);
  handleData('http://' + IP + '/dashboard_lockers', show_dashboard_lockers);
  handleData('http://' + IP + '/dashboard_recent_events', show_dashboard_recent_events);
};

const get_login = function(body) {
  handleData('http://' + IP + '/login', callback_login, 'POST', body);
};

//#endregion

//#region ***********  Event Listeners ***********
// listenTo________________

const listen_to_dropdown = function() {
  document.querySelector('.js-dropdown').addEventListener('click', show_dropdown);
  console.log('Het werkt!');
};

const listen_to_submit = function() {
  document.querySelector('.js-form').addEventListener('submit', function() {
    const body = JSON.stringify({
      username: document.querySelector('#user').value,
      password: document.querySelector('#pass').value
    });

    get_login(body);
  });
};

const listen_to_open = function() {
  let buttons = document.querySelectorAll('.js-open-locker');
  console.log(buttons);
  for (let button of buttons) {
    console.log(button);
    button.addEventListener('click', function() {
      callback_open(button.getAttribute('data-locker'));
    });
  }
};

//#endregion

//#region ***********  INIT / DOMContentLoaded ***********
const init = function() {
  let page = document.querySelector('body').classList.value.split(' ')[0];

  if (page == 'js-dashboard') {
    get_dashboard();
    listen_to_dropdown();
  } else if (page == 'js-lockers') {
    get_lockers();
    listen_to_dropdown();
  } else if (page == 'js-history') {
    get_history();
    listen_to_dropdown();
  } else if (page == 'js-login') {
    listen_to_submit();
  }
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  init();
});

// #endregion
