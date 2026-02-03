const STATUSES = ["Open", "Pending", "Resolved", "Escalated"];

function TicketDetail({ ticket, onStatusChange }) {
  if (!ticket) {
    return (
      <aside className="rounded-2xl border border-dashed border-slate-200 bg-white p-6 text-sm text-slate-500">
        Select a ticket to view details.
      </aside>
    );
  }

  return (
    <aside className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4">
        <p className="text-xs uppercase text-slate-400">Ticket ID</p>
        <p className="text-sm font-semibold text-slate-700">{ticket._id}</p>
      </div>
      <div className="mb-4">
        <p className="text-xs uppercase text-slate-400">User</p>
        <p className="text-sm font-semibold text-slate-700">{ticket.user_id}</p>
      </div>
      <div className="mb-4">
        <p className="text-xs uppercase text-slate-400">Issue</p>
        <p className="text-sm text-slate-600">{ticket.issue}</p>
      </div>
      <div className="mb-6">
        <p className="text-xs uppercase text-slate-400">Priority</p>
        <p className="text-sm font-semibold text-slate-700">{ticket.priority}</p>
      </div>
      <div>
        <p className="mb-2 text-xs uppercase text-slate-400">Update Status</p>
        <div className="grid gap-2">
          {STATUSES.map((status) => (
            <button
              key={status}
              onClick={() => onStatusChange(ticket._id, status)}
              className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
                ticket.status === status
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-indigo-50"
              }`}
            >
              {status}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}

export default TicketDetail;
