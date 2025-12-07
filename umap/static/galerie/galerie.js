export const getGalerie = (point_id) => {
  const settings = JSON.parse(document.getElementById("galerie-settings").dataset.settings)
  const point = settings[point_id]

  if (!point) return ""

  const point_admin_link = point["point_admin_url"] ? `<a href="${point["point_admin_url"]}" target="_blank" class="full_line">Point admin</a>` : ''

  const pictures = point["pictures"].map(p => {
    let code = `<div><a href="${p[0]}" target="_blank"><img src="${p[1]}" alt="" /></a>`
    if (!!p[3]) {
      code += `<a href="${p[3]}" target="_blank">${p[2]}</a>`
    } else {
      code += `<a href="${p[0]}" target="_blank">${p[2]}</a>`
    }
    code += "</div>"
    return code
  })

  return `<div class="content-galerie">${point_admin_link}${pictures.join("")}</div>`
}
