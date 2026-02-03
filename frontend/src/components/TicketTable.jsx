const statusColors = {
  Open: "bg-blue-100 text-blue-700",
  Pending: "bg-amber-100 text-amber-700",
  Resolved: "bg-emerald-100 text-emerald-700",
  Escalated: "bg-rose-100 text-rose-700",
};

function TicketTable({ tickets, onSelect, selectedTicketId }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr>
            <th className="px-4 py-3">User</th>
            <th className="px-4 py-3">Issue</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Priority</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => (
            <tr
              key={ticket._id}
              className={`cursor-pointer border-t ${
                selectedTicketId === ticket._id ? "bg-indigo-50" : "bg-white"
              }`}
              onClick={() => onSelect(ticket)}
            >
              <td className="px-4 py-3 font-medium text-slate-700">
                {ticket.user_id}
              </td>
              <td className="px-4 py-3 text-slate-600">{ticket.issue}</td>
              <td className="px-4 py-3">
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${
                    statusColors[ticket.status] || "bg-slate-100 text-slate-600"
                  }`}
                >
                  {ticket.status}
                </span>
              </td>
              <td className="px-4 py-3 text-slate-600">{ticket.priority}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TicketTable;
