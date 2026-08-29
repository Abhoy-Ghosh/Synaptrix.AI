import React, { useState } from "react"

export default function Sidebar({
  projects,
  activeProjectId,
  activeChatId,
  expandedProjects,
  projectChatsMap,
  onSelectProject,
  onSelectChat,
  onCreateProject,
  onDeleteProject,
  onCreateChat,
  onDeleteChat,
  isOpen,
  onToggleSidebar
}) {
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)
  const [newProjName, setNewProjName] = useState("")
  const [newProjTopic, setNewProjTopic] = useState("")

  const [showNewChatModal, setShowNewChatModal] = useState(null) // projectId or null
  const [newChatTitle, setNewChatTitle] = useState("")
  const [newChatMode, setNewChatMode] = useState("parallel")

  const handleProjectSubmit = (e) => {
    e.preventDefault()
    if (!newProjName.trim() || !newProjTopic.trim()) return
    onCreateProject(newProjName.trim(), newProjTopic.trim())
    setNewProjName("")
    setNewProjTopic("")
    setShowNewProjectModal(false)
  }

  const handleChatSubmit = (e, projectId) => {
    e.preventDefault()
    if (!newChatTitle.trim()) return
    onCreateChat(projectId, newChatTitle.trim(), newChatMode)
    setNewChatTitle("")
    setShowNewChatModal(null)
  }

  return (
    <aside className={`workspace-sidebar ${isOpen ? "open" : "collapsed"}`}>
      <div className="sidebar-header">
        <div className="brand-badge">
          <span className="brand-logo">🧠</span>
          <span className="brand-title">Workspaces</span>
        </div>
        <button 
          className="sidebar-toggle-btn"
          onClick={onToggleSidebar}
          title={isOpen ? "Collapse Sidebar" : "Expand Sidebar"}
        >
          {isOpen ? "◀" : "▶"}
        </button>
      </div>

      {isOpen && (
        <div className="sidebar-content">
          <button 
            className="btn-create-project"
            onClick={() => setShowNewProjectModal(true)}
          >
            <span className="btn-icon">+</span> New Project
          </button>

          {/* NEW PROJECT MODAL */}
          {showNewProjectModal && (
            <div className="sidebar-modal-overlay">
              <form className="sidebar-modal" onSubmit={handleProjectSubmit}>
                <h3>Create New Project</h3>
                <input 
                  type="text" 
                  placeholder="Project Name (e.g. Quantum AI)" 
                  value={newProjName}
                  onChange={(e) => setNewProjName(e.target.value)}
                  autoFocus
                  required
                />
                <input 
                  type="text" 
                  placeholder="Topic Area (e.g. Quantum Computing)" 
                  value={newProjTopic}
                  onChange={(e) => setNewProjTopic(e.target.value)}
                  required
                />
                <div className="modal-actions">
                  <button type="button" className="btn-cancel" onClick={() => setShowNewProjectModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn-submit">
                    Create
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="projects-list">
            {projects.length === 0 ? (
              <div className="sidebar-empty">
                No projects yet. Click <strong>+ New Project</strong> to start!
              </div>
            ) : (
              projects.map((proj) => {
                const isSelectedProj = activeProjectId === proj.id
                const isExpanded = expandedProjects[proj.id]
                const chats = projectChatsMap[proj.id] || []

                return (
                  <div 
                    key={proj.id} 
                    className={`project-group ${isSelectedProj ? "active-project" : ""}`}
                  >
                    <div 
                      className="project-item"
                      onClick={() => onSelectProject(proj.id)}
                    >
                      <span className="project-arrow">{isExpanded ? "▼" : "▶"}</span>
                      <div className="project-info">
                        <span className="project-name">{proj.name}</span>
                        <span className="project-topic">{proj.topic}</span>
                      </div>
                      <button 
                        className="btn-delete-item"
                        title="Delete Project"
                        onClick={(e) => {
                          e.stopPropagation()
                          if (confirm(`Delete project "${proj.name}" and all chats?`)) {
                            onDeleteProject(proj.id)
                          }
                        }}
                      >
                        ✕
                      </button>
                    </div>

                    {isExpanded && (
                      <div className="chats-tree">
                        <button 
                          className="btn-add-chat"
                          onClick={() => setShowNewChatModal(proj.id)}
                        >
                          + New Chat
                        </button>

                        {/* NEW CHAT MODAL */}
                        {showNewChatModal === proj.id && (
                          <form className="mini-chat-form" onSubmit={(e) => handleChatSubmit(e, proj.id)}>
                            <input 
                              type="text" 
                              placeholder="Chat Title (e.g. Error Correction)" 
                              value={newChatTitle}
                              onChange={(e) => setNewChatTitle(e.target.value)}
                              autoFocus
                              required
                            />
                            <select 
                              value={newChatMode} 
                              onChange={(e) => setNewChatMode(e.target.value)}
                            >
                              <option value="parallel">⚡ Parallel Mode</option>
                              <option value="research">🧠 Deep Research</option>
                              <option value="fast">🚀 Fast Mode</option>
                            </select>
                            <div className="mini-actions">
                              <button type="button" onClick={() => setShowNewChatModal(null)}>Cancel</button>
                              <button type="submit">Save</button>
                            </div>
                          </form>
                        )}

                        {chats.map((chat) => (
                          <div 
                            key={chat.id} 
                            className={`chat-item ${activeChatId === chat.id ? "active-chat" : ""}`}
                            onClick={() => onSelectChat(proj.id, chat.id)}
                          >
                            <span className="chat-icon">💬</span>
                            <span className="chat-title">{chat.title}</span>
                            <button 
                              className="btn-delete-item"
                              title="Delete Chat"
                              onClick={(e) => {
                                e.stopPropagation()
                                onDeleteChat(proj.id, chat.id)
                              }}
                            >
                              ✕
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )
              })
            )}
          </div>
        </div>
      )}
    </aside>
  )
}
