// ============================================
// PURE NODE.JS TEST (NO EXTERNAL LIBRARIES)
// ============================================
//
// Run:
// node test.js
//
// Then open:
// http://localhost:3000
//
// ============================================

const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");

// ============================================
// DUMMY DATA
// ============================================

const startupData = [
  { month: "Jan", revenue: 1200, expenses: 900, users: 50 },
  { month: "Feb", revenue: 1800, expenses: 1100, users: 80 },
  { month: "Mar", revenue: 2500, expenses: 1500, users: 120 },
  { month: "Apr", revenue: 3200, expenses: 1700, users: 170 },
  { month: "May", revenue: 4100, expenses: 2100, users: 240 },
  { month: "Jun", revenue: 5300, expenses: 2600, users: 320 }
];

// ============================================
// PROCESS DATA
// ============================================

const processedData = startupData.map(item => ({
  ...item,
  profit: item.revenue - item.expenses
}));

// ============================================
// SAVE JSON FILE TEST
// ============================================

fs.writeFileSync(
  path.join(__dirname, "startup_data.json"),
  JSON.stringify(processedData, null, 2)
);

console.log("✅ JSON file created");

// ============================================
// SYSTEM INFO
// ============================================

console.log("\n=== SYSTEM INFO ===");
console.log("Node Version:", process.version);
console.log("Platform:", process.platform);
console.log("CPU Cores:", os.cpus().length);
console.log("RAM:", Math.round(os.totalmem() / 1e9), "GB");

// ============================================
// CALCULATIONS
// ============================================

const totalRevenue = processedData.reduce(
  (sum, item) => sum + item.revenue,
  0
);

const totalExpenses = processedData.reduce(
  (sum, item) => sum + item.expenses,
  0
);

const totalUsers = processedData.reduce(
  (sum, item) => sum + item.users,
  0
);

console.log("\n=== CALCULATIONS ===");
console.log("Total Revenue:", totalRevenue);
console.log("Total Expenses:", totalExpenses);
console.log("Total Users:", totalUsers);

// ============================================
// CREATE WEB PAGE
// ============================================

const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Node.js Test</title>

  <style>
    body {
      font-family: Arial;
      background: #0f172a;
      color: white;
      padding: 40px;
    }

    h1 {
      color: #38bdf8;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #334155;
      padding: 10px;
    }

    th {
      background: #1e293b;
    }

    .card {
      background: #1e293b;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 20px;
    }
  </style>
</head>

<body>

  <h1>🚀 Pure Node.js Test</h1>

  <div class="card">
    <h2>System Info</h2>

    <p><strong>Node Version:</strong> ${process.version}</p>
    <p><strong>Platform:</strong> ${process.platform}</p>
    <p><strong>CPU Cores:</strong> ${os.cpus().length}</p>
  </div>

  <div class="card">
    <h2>Startup Data</h2>

    <table>
      <tr>
        <th>Month</th>
        <th>Revenue</th>
        <th>Expenses</th>
        <th>Users</th>
        <th>Profit</th>
      </tr>

      ${processedData.map(item => `
        <tr>
          <td>${item.month}</td>
          <td>$${item.revenue}</td>
          <td>$${item.expenses}</td>
          <td>${item.users}</td>
          <td>$${item.profit}</td>
        </tr>
      `).join("")}

    </table>
  </div>

  <div class="card">
    <h2>Calculations</h2>

    <p><strong>Total Revenue:</strong> $${totalRevenue}</p>
    <p><strong>Total Expenses:</strong> $${totalExpenses}</p>
    <p><strong>Total Users:</strong> ${totalUsers}</p>
  </div>

</body>
</html>
`;

// ============================================
// CREATE SERVER
// ============================================

const server = http.createServer((req, res) => {

  if (req.url === "/api/data") {

    res.writeHead(200, {
      "Content-Type": "application/json"
    });

    res.end(JSON.stringify(processedData, null, 2));

    return;
  }

  res.writeHead(200, {
    "Content-Type": "text/html"
  });

  res.end(html);
});

// ============================================
// START SERVER
// ============================================

const PORT = 3000;

server.listen(PORT, () => {

  console.log("\n=================================");
  console.log("✅ NODE.JS TEST SERVER RUNNING");
  console.log("=================================");
  console.log(`🌐 Open: http://localhost:${PORT}`);
  console.log(`📦 API : http://localhost:${PORT}/api/data`);
  console.log("=================================\n");

});