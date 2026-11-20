const API = "https://gym-management-system-ehl4.onrender.com";
let currentPage = "dashboard";
const $ = s => document.querySelector(s);
const money = n => "₹" + Number(n||0).toLocaleString("en-IN");
function toast(msg){const t=$("#toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2600)}
async function api(path, opts={}) {
  const headers={"Content-Type":"application/json",...(token?{Authorization:`Bearer ${token}`}:{}) ,...(opts.headers||{})};
  const res=await fetch(API+path,{...opts,headers});
  if(res.status===401){showLogin();throw new Error("Please sign in again")}
  const data=await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data.detail||"Request failed");
  return data;
}
function showLogin(){ $("#login-panel").classList.remove("hidden"); }
function hideLogin(){ $("#login-panel").classList.add("hidden"); }
$("#login-form").addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(e.target);try{const d=await api("/auth/login",{method:"POST",body:JSON.stringify({email:f.get("email"),password:f.get("password")})});token=d.access_token;localStorage.setItem("fitflow_token",token);hideLogin();loadDashboard();toast("Signed in successfully")}catch(err){toast(err.message)}});
$("#logout").onclick=()=>{token="";localStorage.removeItem("fitflow_token");showLogin()};
$("#today").textContent=new Date().toLocaleDateString("en-IN",{weekday:"short",day:"numeric",month:"short",year:"numeric"});
function stat(label,value,icon,sub){return `<div class="stat"><div class="stat-top"><span>${label}</span><span class="stat-icon">${icon}</span></div><strong>${value}</strong><small>${sub}</small></div>`}
async function loadDashboard(){try{const d=await api("/dashboard/summary");$("#stats").innerHTML=stat("Total members",d.total_members,"♙","Registered members")+stat("Active memberships",d.active_memberships,"◷","Currently active")+stat("Today's attendance",d.today_attendance,"✓","Check-ins recorded today")+stat("Monthly revenue",money(d.monthly_revenue),"₹",`${d.pending_payments} pending payments`);const m=await api("/members/?limit=6");$("#recent-members").innerHTML=table(["Member","Email","Phone","Status"],m.map(x=>[x.full_name,x.email,x.phone,`<span class="pill">${x.is_active?"Active":"Inactive"}</span>`]));}catch(e){toast(e.message)}}
function table(headers,rows){if(!rows.length)return '<p class="muted">No records yet. Add your first record to get started.</p>';return `<table><thead><tr>${headers.map(h=>`<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(v=>`<td>${v??""}</td>`).join("")}</tr>`).join("")}</tbody></table>`}
const pages={
members:{title:"Members",path:"/members/",fields:[["full_name","Full name"],["email","Email","email"],["phone","Phone"],["age","Age","number"],["gender","Gender"],["notes","Notes"]],headers:["Name","Email","Phone","Age","Status"],map:x=>[x.full_name,x.email,x.phone,x.age,x.is_active?"Active":"Inactive"]},
trainers:{title:"Trainers",path:"/trainers/",fields:[["full_name","Full name"],["email","Email","email"],["phone","Phone"],["specialization","Specialization"],["experience_years","Experience (years)","number"]],headers:["Name","Email","Specialization","Experience"],map:x=>[x.full_name,x.email,x.specialization,x.experience_years+" yrs"]},
memberships:{title:"Membership plans",path:"/plans/",fields:[["name","Plan name"],["duration_days","Duration (days)","number"],["price","Price (₹)","number"],["description","Description"]],headers:["Plan","Duration","Price","Status"],map:x=>[x.name,x.duration_days+" days",money(x.price),x.is_active?"Active":"Inactive"]},
payments:{title:"Payments",path:"/payments/",fields:[["member_id","Member ID","number"],["membership_id","Membership ID (optional)","number"],["amount","Amount (₹)","number"],["method","Method (Cash / UPI / Card)"],["status","Status (paid / pending)"],["reference","Reference"]],headers:["Member ID","Amount","Date","Method","Status"],map:x=>[x.member_id,money(x.amount),x.payment_date,x.method,x.status]},
attendance:{title:"Attendance",path:"/attendance/",fields:[["member_id","Member ID","number"],["notes","Notes"]],headers:["Member ID","Check in","Check out","Notes"],map:x=>[x.member_id,new Date(x.check_in).toLocaleString(),x.check_out?new Date(x.check_out).toLocaleString():"Still in",x.notes]},
workouts:{title:"Workout plans",path:"/workouts/",fields:[["member_id","Member ID","number"],["trainer_id","Trainer ID (optional)","number"],["title","Plan title"],["details","Workout details"]],headers:["Member ID","Title","Details","Start date"],map:x=>[x.member_id,x.title,x.details,x.start_date]},
diet:{title:"Diet plans",path:"/diet-plans/",fields:[["member_id","Member ID","number"],["trainer_id","Trainer ID (optional)","number"],["title","Plan title"],["details","Diet details"]],headers:["Member ID","Title","Details","Start date"],map:x=>[x.member_id,x.title,x.details,x.start_date]}
};
async function openPage(page){currentPage=page;$("#content").classList.add("hidden");$("#page-content").classList.remove("hidden");const cfg=pages[page];$("#page-title").textContent=cfg.title;$("#page-content").innerHTML=`<div class="page-head"><div><h2>${cfg.title}</h2><p class="muted">Manage your gym ${cfg.title.toLowerCase()}.</p></div></div><div class="panel form-panel"><div class="panel-head"><div><h3>Add new record</h3><p>Complete the details below and save.</p></div></div><form id="record-form" class="form-grid">${cfg.fields.map(([n,l,t])=>`<label>${l}<input name="${n}" ${t?`type="${t}"`:""} ${t==="number"?'min="0" step="any"':""} ${n==="email"?"required":""}></label>`).join("")}<button class="primary">Save record</button></form></div><div class="panel"><div class="panel-head"><div><h3>All records</h3><p>Latest records from the database</p></div><button class="text-button" id="refresh">Refresh ↻</button></div><div id="page-table" class="table-wrap">Loading…</div></div>`;
$("#record-form").onsubmit=async e=>{e.preventDefault();const fd=new FormData(e.target),obj={};for(const [k,v] of fd.entries()){if(v!=="")obj[k]=["age","experience_years","duration_days","price","member_id","membership_id","trainer_id"].includes(k)?Number(v):v}try{let path=cfg.path,method="POST";if(page==="attendance"){path="/attendance/check-in"}const result=await api(path,{method,body:JSON.stringify(obj)});toast("Record saved");e.target.reset();loadTable(page)}catch(err){toast(err.message)}};
$("#refresh").onclick=()=>loadTable(page);loadTable(page)}
async function loadTable(page){const cfg=pages[page];try{let d=await api(cfg.path);$("#page-table").innerHTML=table(cfg.headers,d.map(cfg.map));}catch(e){$("#page-table").textContent=e.message}}
function go(page){document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.page===page));if(page==="dashboard"){currentPage="dashboard";$("#page-title").textContent="Dashboard";$("#page-content").classList.add("hidden");$("#content").classList.remove("hidden");loadDashboard()}else openPage(page)}
document.querySelectorAll("[data-page]").forEach(b=>b.onclick=()=>go(b.dataset.page));
document.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>go(b.dataset.go));
$("#quick-add").onclick=()=>go("members");
if(!token)showLogin();else loadDashboard();
