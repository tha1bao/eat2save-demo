"""Thêm định dạng 'Món lẻ' (ITEM) vào demo Eat2Save và áp dụng bậc 10% cho mọi cửa hàng mới.
Chạy: python3 tools/patch_mon_le.py <thư mục chứa core.js, customer.js, merchant.js>"""
import sys, os
D = sys.argv[1]
def load(k): return open(os.path.join(D, k + '.js'), encoding='utf-8').read()
def save(k, s): open(os.path.join(D, k + '.js'), 'w', encoding='utf-8').write(s)
def rep(s, old, new, count=1):
    n = s.count(old)
    assert n == count, (old[:80], n)
    return s.replace(old, new)

# ---------- core ----------
c = load('core')
c = rep(c, '"e2s.db.v4"', '"e2s.db.v5"')                      # dữ liệu mẫu mới
c = rep(c, 'n<=52&&t.introEligible?', 'n<=52?')                # 5% → 10% → 15% cho mọi cửa hàng mới (Phần 7)
c = rep(c, 't.comboTag=t=>"Combo "+(t.size||"M")',
        't.comboTag=e=>"ITEM"===e.format?r("Món lẻ","Single item"):"Combo "+(e.size||"M")')
c = rep(c, 't.comboLabel=e=>"Combo "+(e.size||"M")+" · "+t.catName(e.cat)',
        't.comboLabel=e=>t.comboTag(e)+" · "+t.catName(e.cat)')
c = rep(c, 't.validateListing=e=>{',
        't.validateListing=e=>"ITEM"===e.format?t.validateItem(e):t.validateCombo(e),t.validateCombo=e=>{')
c = rep(c, 'format:"COMBO",cat:n.cat,size:n.size',
        'format:n.format||"COMBO",cat:n.cat,size:"ITEM"===n.format?null:n.size', count=2)
c = rep(c, 'const l=n.name&&n.name.trim()?n.name:"Combo "+n.size+" · "+f[n.cat].vi',
        'const l=n.name&&n.name.trim()?n.name:"ITEM"===n.format?i[0]&&i[0].n||"Món lẻ":"Combo "+n.size+" · "+f[n.cat].vi')
c = rep(c, 'nameEn:n.nameEn||l', 'nameEn:n.nameEn||("ITEM"===n.format&&i[0]?i[0].nEn||l:l)')
c = rep(c, 'format:"COMBO",cat:c.cat,size:c.size', 'format:c.format||"COMBO",cat:c.cat,size:c.size')
seed = ('["t1","t2","t4","t5","t6","t7","t8","t9","t10"].forEach((t=>u(t))),'
        '[{id:"t11",s:"s1",cat:"SWEET",icon:"cake",name:"Hộp tart trứng (4 cái)",nameEn:"Egg tart box (4 pcs)",'
        'items:[l(1,"Hộp tart trứng (4 cái)","Egg tart box (4 pcs)",4e4)],price:28e3,'
        'allergens:"Gluten, sữa, trứng",allergensEn:"Gluten, milk, egg",storage:"Nhiệt độ phòng, dùng trong ngày",'
        'storageEn:"Room temperature, eat today",made:"07:00 sáng nay",madeEn:"07:00 this morning",kg:.3,'
        'start:"20:00",end:"21:30",qty:4,days:[1,2,3,4,5,6]},'
        '{id:"t12",s:"s2",cat:"SWEET",icon:"croissant",name:"Croissant hạnh nhân",nameEn:"Almond croissant",'
        'items:[l(1,"Croissant hạnh nhân","Almond croissant",3e4)],price:21e3,'
        'allergens:"Gluten, sữa, trứng, hạnh nhân",allergensEn:"Gluten, milk, egg, almond",'
        'storage:"Nhiệt độ phòng, dùng trong ngày",storageEn:"Room temperature, eat today",'
        'made:"06:30 sáng nay",madeEn:"06:30 this morning",kg:.12,start:"21:00",end:"22:00",qty:6,days:[1,2,3,4,5,6,7]}]'
        '.forEach((e=>{e.format="ITEM",e.size=null,e.original=t.itemsTotal(e.items),e.contents=t.itemsText(e.items),'
        'e.contentsEn=t.itemsText(e.items,!0),d.templates[e.id]=Object.assign({},e),u(e.id)}))')
c = rep(c, '["t1","t2","t4","t5","t6","t7","t8","t9","t10"].forEach((t=>u(t)))', seed)
c += r''';(function(t){var r=t.L,E=t.RULES;t.validateItem=function(e){var n=[],it=(e.items||[]).filter(function(x){return(x.n||x.nEn||"").trim()||x.p}).slice(0,1),s=it.length?(Number(it[0].p)||0):0,i=Number(String(e.price==null?"":e.price).replace(/\D/g,""))||0,c=t.discount(s,i);if(!it.length)n.push(r("Nhập tên món và giá niêm yết","Enter the item name and usual price"));else if(!((it[0].n||it[0].nEn||"").trim()&&s>0))n.push(r("Món cần tên và giá niêm yết","The item needs a name and usual price"));else if(!(i>0))n.push(r("Nhập giá bán món lẻ","Enter the selling price"));else if(c<E.recMin-1e-9)n.push(r("Giảm "+Math.round(100*c)+"% – món lẻ phải giảm ít nhất 20%","Only "+Math.round(100*c)+"% off – single items need at least 20% off"));else if(c>E.maxDiscount+1e-9)n.push(r("Giảm "+Math.round(100*c)+"% – vượt trần 40%","Over the 40% cap ("+Math.round(100*c)+"% off)"));e.allergens&&e.allergens.trim()||n.push(r("Thiếu thông tin dị ứng","Missing allergen information"));e.storage&&e.storage.trim()||n.push(r("Thiếu hướng dẫn bảo quản","Missing storage instructions"));e.qty>=1||n.push(r("Số lượng tối thiểu là 1","Quantity must be at least 1"));e.start>=e.end&&n.push(r("Giờ kết thúc phải sau giờ bắt đầu","Pickup end must be after start"));var d=((e.name||"")+" "+it.map(function(x){return x.n+" "+(x.nEn||"")}).join(" ")).toLowerCase();E.banned.some(function(b){return d.indexOf(b)>=0})&&n.push(r("Danh mục bị cấm (đồ sống, đồ uống có cồn…)","Banned category (raw food, alcohol…)"));return{ok:0===n.length,errors:n,warns:[],disc:c,orig:s,price:i,combo:null}}})(window.E2S);'''
save('core', c)

# ---------- customer ----------
u = load('customer')
u = rep(u, '(!i.format||a.size===i.format)', '(!i.format||("ITEM"===i.format?"ITEM"===a.format:a.size===i.format))')
u = rep(u, 'r("format","L","Combo L · 45k")', 'r("format","L","Combo L · 45k")}${r("format","ITEM",a("Món lẻ","Single item"))')
u = rep(u, 'a("Bên trong combo","Inside this combo")', '"ITEM"===l.format?a("Chi tiết món","Item details"):a("Bên trong combo","Inside this combo")')
u = rep(u, 'a("Giá gốc (tổng các món)","Original value (sum of items)")', '"ITEM"===l.format?a("Giá niêm yết","Usual price"):a("Giá gốc (tổng các món)","Original value (sum of items)")')
u = rep(u, 'a("Giá ","Price ")}${E2S.comboTag(l)}', '"ITEM"===l.format?a("Giá bán","Selling price"):a("Giá ","Price ")+E2S.comboTag(l)}')
u = rep(u, 'a("Cỡ combo","Combo size")', 'a("Loại deal","Deal type")')
save('customer', u)

# ---------- merchant ----------
m = load('merchant')
m = rep(m, 'return{templateId:a||null,cat:s.cat,size:s.size,', 'return{templateId:a||null,format:s.format||"COMBO",price:"ITEM"===s.format?s.price:0,cat:s.cat,size:s.size||"M",')
m = rep(m, 'combo:a=>{', 'ffmt:a=>{const s=e.form;s.format=a.dataset.v,"ITEM"===s.format&&(s.items=s.items.slice(0,1),s.items[0].q=1,s.price||(s.price=1e3*Math.round(.7*(s.items[0].p||0)/1e3))),E2S.rerender()},combo:a=>{')
m = rep(m, 'a.size===s.size&&a.cat===s.cat||', 'a.size===s.size&&a.cat===s.cat&&(a.format||"COMBO")===s.format||')
m = rep(m, 'o("sz",`(Combo ${t.size})`)', 'o("sz","ITEM"===t.format?"":`(Combo ${t.size})`)')
fmt = ('<div><div class="small mb8">${a("Hình thức","Format")}</div><div class="row gap6">'
       '<button class="opt f1 ${"ITEM"!==t.format?"on":""}" style="padding:6px 4px;text-align:center" data-act="ffmt" data-v="COMBO"><b>Combo S/M/L</b><br><span class="xs muted">${a("giá cố định theo cỡ","fixed price by size")}</span></button>'
       '<button class="opt f1 ${"ITEM"===t.format?"on":""}" style="padding:6px 4px;text-align:center" data-act="ffmt" data-v="ITEM"><b>${a("Món lẻ","Single item")}</b><br><span class="xs muted">${a("tự đặt giá, giảm 20–40%","own price, 20–40% off")}</span></button></div></div>\\n        ')
old_card = '<div class="card col gap12">\\n        <div><div class="small mb8">${a("Nhóm sản phẩm","Product group")}</div>'
m = rep(m, old_card, '<div class="card col gap12">\\n        ' + fmt + '<div><div class="small mb8">${a("Nhóm sản phẩm","Product group")}</div>')
i0 = m.index('<div><div class="small mb8">${a("Cỡ combo · giá bán cố định"')
end_mark = '.join("")}</div></div>'
i1 = m.index(end_mark, i0) + len(end_mark)
size_block = m[i0:i1]
price_block = '<label class="fld">${a("Giá bán món lẻ (đ)","Item selling price (VND)")}<input class="input" data-f="price" inputmode="numeric" value="${t.price||""}"></label>'
m = m[:i0] + '${"ITEM"===t.format?`' + price_block + '`:`' + size_block + '`}' + m[i1:]
m = rep(m, '${a("Bên trong combo (giá niêm yết thường ngày)","Inside the combo (usual shelf prices)")}',
        '${"ITEM"===t.format?a("Món (giá niêm yết thường ngày)","Item (usual shelf price)"):a("Bên trong combo (giá niêm yết thường ngày)","Inside the combo (usual shelf prices)")}')
m = rep(m, '${t.items.map(h).join("")}', '${("ITEM"===t.format?t.items.slice(0,1):t.items).map(h).join("")}')
btn = '<button class="chip" style="align-self:flex-start;height:32px" data-act="iadd">+ ${a("Thêm món","Add item")}</button>'
m = rep(m, btn, '${"ITEM"===t.format?"":`' + btn + '`}')
m = rep(m, '${a("Giá gốc = tổng các món","Original value = sum of items")}', '${"ITEM"===t.format?a("Giá niêm yết","Usual price"):a("Giá gốc = tổng các món","Original value = sum of items")}')
m = rep(m, '${a("Số combo hôm nay","Combos today")}', '${"ITEM"===t.format?a("Số suất hôm nay","Units today"):a("Số combo hôm nay","Combos today")}')
m = rep(m, '${a("Đăng combo","Publish combo")}', '${"ITEM"===t.format?a("Đăng món lẻ","Publish item"):a("Đăng combo","Publish combo")}')
m = rep(m, 'a("Mỗi combo bạn nhận ≈ ","You receive ≈ ")', '"ITEM"===t.format?a("Mỗi suất bạn nhận ≈ ","You receive ≈ "):a("Mỗi combo bạn nhận ≈ ","You receive ≈ ")')
save('merchant', m)
print("patched")
