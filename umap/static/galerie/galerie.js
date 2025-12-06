export const getGalerie = (point_id) => {
  const settings = JSON.parse(document.getElementById("galerie-settings").dataset.settings)
  const point = settings[point_id]

  const point_admin_link = `<a href="${point["point_admin_url"]}" target="_blank" class="full_line">Point admin</a>`

  const pictures = point["pictures"].map(p => {
    return `<div><a href="${p[0]}" target="_blank"><img src="${p[1]}" alt="" /></a><a href="${p[3]}" target="_blank">${p[2]}</a></div>`
  })

  return `<div class="content-galerie">${point_admin_link}${pictures.join("")}</div>`
}
