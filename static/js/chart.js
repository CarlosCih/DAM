    const API = {
      summary: "/api/metrics/summary/",
      createdSeries: "/api/metrics/timeseries/?metric=created",
      statusBreakdown: "/api/metrics/breakdown/?by=status",
    };

    function qParams() {
      const from = document.getElementById("fromDate").value;
      const to = document.getElementById("toDate").value;
      const p = new URLSearchParams();
      if (from) p.set("from", from);
      if (to) p.set("to", to);
      const qs = p.toString();
      return qs ? `?${qs}` : "";
    }

    async function fetchJson(url) {
      const res = await fetch(url, { headers: { "Accept": "application/json" } });
      if (!res.ok) throw new Error(`HTTP ${res.status} en ${url}`);
      return await res.json();
    }

    // Charts (se crean una vez y se actualizan)
    let createdChart = null;
    let statusChart = null;

    function normalizeChartData(data) {
      const labels = Array.isArray(data?.labels)
        ? data.labels
        : (Array.isArray(data?.label) ? data.label : []);
      const datasets = Array.isArray(data?.datasets) ? data.datasets : [];
      return { labels, datasets };
    }

    function hasChartData(data) {
      const normalized = normalizeChartData(data);
      const labels = normalized.labels;
      const datasets = normalized.datasets;
      const values = datasets.flatMap(ds => Array.isArray(ds?.data) ? ds.data : []);
      const hasValues = values.some(v => Number(v) > 0);
      return labels.length > 0 && values.length > 0 && hasValues;
    }

    function setChartEmptyState(canvasId, isEmpty, message) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const card = canvas.closest(".card");
      if (!card) return;

      let emptyNode = card.querySelector(".chart-empty");

      if (isEmpty) {
        canvas.style.display = "none";
        if (!emptyNode) {
          emptyNode = document.createElement("div");
          emptyNode.className = "chart-empty";
          card.appendChild(emptyNode);
        }
        emptyNode.textContent = message;
      } else {
        canvas.style.display = "block";
        if (emptyNode) emptyNode.remove();
      }
    }

    function ensureLineChart(ctx, data) {
      if (!createdChart) {
        createdChart = new Chart(ctx, {
          type: "line",
          data,
          options: {
            responsive: true,
            plugins: { legend: { display: true } },
            scales: { y: { beginAtZero: true } }
          }
        });
      } else {
        createdChart.data = data;
        createdChart.update();
      }
    }

    function ensureDoughnutChart(ctx, data) {
      if (!statusChart) {
        statusChart = new Chart(ctx, {
          type: "doughnut",
          data,
          options: {
            responsive: true,
            plugins: { legend: { position: "bottom" } }
          }
        });
      } else {
        statusChart.data = data;
        statusChart.update();
      }
    }

    async function loadDashboard() {
      const qs = qParams();

      // 1) Summary → KPIs
      const s = await fetchJson(API.summary + qs);
      document.getElementById("kpiTotal").textContent = s.total;
      document.getElementById("kpiOpen").textContent = s.open;
      document.getElementById("kpiProgress").textContent = s.in_progress;
      document.getElementById("kpiReopened").textContent = s.reopened;
      document.getElementById("kpiAvg").textContent = (s.avg_resolution_hours ?? "—");

      // 2) Created timeseries → line chart
      const created = await fetchJson(API.createdSeries + (qs ? "&" + qs.slice(1) : ""));
      const createdIsEmpty = !hasChartData(created);
      setChartEmptyState("chartCreated", createdIsEmpty, "Sin datos de tickets creados para el rango seleccionado.");
      if (!createdIsEmpty) {
        ensureLineChart(document.getElementById("chartCreated"), normalizeChartData(created));
      }

      // 3) Status breakdown → doughnut chart
      const status = await fetchJson(API.statusBreakdown + (qs ? "&" + qs.slice(1) : ""));
      const statusIsEmpty = !hasChartData(status);
      setChartEmptyState("chartStatus", statusIsEmpty, "Sin distribución de estatus para el rango seleccionado.");
      if (!statusIsEmpty) {
        ensureDoughnutChart(document.getElementById("chartStatus"), normalizeChartData(status));
      }
    }

    // Defaults: últimos 30 días
    function formatLocalDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    }

    function setDefaultDates() {
      const today = new Date();
      const to = formatLocalDate(today);
      const fromDate = new Date(today);
      fromDate.setDate(today.getDate() - 30);
      const from = formatLocalDate(fromDate);

      document.getElementById("fromDate").value = from;
      document.getElementById("toDate").value = to;
    }

    document.getElementById("btnApply").addEventListener("click", () => {
      loadDashboard().catch(err => alert(err.message));
    });

    setDefaultDates();
    loadDashboard().catch(err => alert(err.message));
