import { useEffect, useState } from "react";

import TicketDetail from "./components/TicketDetail";
import TicketTable from "./components/TicketTable";

const STATUSES = ["All", "Open", "Pending", "Resolved", "Escalated"];

function App() {
  const [tickets, setTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [statusFilter, setStatusFilter] = useState("All");

  const fetchTickets = async (status = "All") => {
    try {
      const query = status !== "All" ? `?status=${status}` : "";
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/admin/tickets${query}`
      );
      const data = await response.json();
      setTickets(data);
      if (data.length > 0) {
        setSelectedTicket(data[0]);
      } else {
        setSelectedTicket(null);
      }
    } catch (error) {
      console.error("Failed to fetch tickets", error);
      setTickets([]);
      setSelectedTicket(null);
    }
  };

  useEffect(() => {
    fetchTickets(statusFilter);
  }, [statusFilter]);

  const handleStatusChange = async (ticketId, status) => {
    try {
      await fetch(`${import.meta.env.VITE_API_URL}/tickets/${ticketId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      fetchTickets(statusFilter);
    } catch (error) {
      console.error("Failed to update ticket", error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between p-6">
          <div>
            <h1 className="text-2xl font-bold">Support AI Admin</h1>
            <p className="text-sm text-slate-500">
              Monitor tickets and escalation trends.
            </p>
          </div>
          <div className="rounded-full bg-indigo-100 px-4 py-2 text-sm font-semibold text-indigo-700">
            MVP Dashboard
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-6xl gap-6 p-6 lg:grid-cols-[2fr,1fr]">
        <section>
          <div className="mb-4 flex items-center gap-3">
            {STATUSES.map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                  statusFilter === status
                    ? "bg-indigo-600 text-white"
                    : "bg-white text-slate-600 hover:bg-indigo-50"
                }`}
              >
                {status}
              </button>
            ))}
          </div>
          <TicketTable
            tickets={tickets}
            onSelect={setSelectedTicket}
            selectedTicketId={selectedTicket?._id}
          />
        </section>

        <TicketDetail
          ticket={selectedTicket}
          onStatusChange={handleStatusChange}
        />
      </main>
    </div>
  );
}

export default App;
