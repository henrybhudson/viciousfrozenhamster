// // Create the chart
// const COLOURS = {
//     "Bills": "#10451D",
//     "Charity": "#155D27",
//     "Food": "#1A7431",
//     "Entertainment": "#208B3A",
//     "Finances": "#25A244",
//     "General": "#2DC653",
//     "Groceries": "#4AD66D",
//     "Holidays": "#6EDE8A",
//     "Personal Care": "#92E6A7",
//     "Shopping": "#B7EFC5",
//     "Bank Transfers": "#C9F2D3",
//     "Transport": "#E8FFEE"
// }

// const CATEGORIES = ["Bills", "Charity", "Food", "Entertainment", "Finances", "General", "Groceries", "Holidays", "Personal Care", "Shopping", "Bank Transfers", "Transport"];


// const createData = (transactions) => {
//     let values = {};
//     let res = [];
//     CATEGORIES.forEach((category) => {
//         values[category] = 0
//     });

//     transactions.forEach((transaction) => {
//         values[transaction["category"]] += parseFloat(transaction["price"]);
//     });

//     for (const [category, value] of Object.entries(values)) {
//         res.push([category, value]);
//     }

//     return res;
// };

// const f = () => {
//     const CIRCLE_SIZE = (window.innerWidth < 500) ? "120%" : "100%";

//     Highcharts.chart('container', {
//         chart: {
//             renderTo: 'container',
//             type: 'pie',
//             backgroundColor: 'transparent',
//         },
//         plotOptions: {
//             pie: {
//                 shadow: false
//             }
//         },
//         tooltip: {
//             formatter: function () {
//                 return '<b>' + this.point.name + '</b>: ' + this.y + ' %';
//             }
//         },
//         series: [{
//             name: 'Expenses',
//             data: [["Entertainment", 0.4], ["Personal Care", 1], ["Transport", 1.5], ["Food", 2], ["Groceries", 3], ["Available", 4]],
//             size: CIRCLE_SIZE,
//             innerSize: '80%',
//             dataLabels: {
//                 enabled: false
//             }
//         }],
//         credits: {
//             enabled: false
//         },
//         title: {
//             text: ""
//         }
//     });
// }

// f();