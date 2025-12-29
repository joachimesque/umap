import * as Utils from '../umap/js/modules/utils.js'

export const getGalerieLinks = (point_id) => {
  const can_edit = JSON.parse(document.getElementById("map-settings").dataset.settings)["properties"]["editMode"] != "disabled"

  const point_admin_link = can_edit ? `<a href="${Utils.getAdminUrl(point_id)}" target="_blank">🖊️ Admin</a>` : ""
  const point_detail_link = `<a href="${Utils.getGalerieUrl(point_id)}" target="_blank">🔎 Détails</a>`
  const point_upload_link = `<a href="${Utils.getGalerieUploadUrl(point_id)}" target="_blank" data-dialog-upload-back="map" data-dialog-upload="${point_id}">🌇 Upload</a>`

  return `<div class="content-galerie_links">${point_admin_link}${point_detail_link}${point_upload_link}</div>`
}
export const getGalerie = (point_id) => {
  const settings = JSON.parse(document.getElementById("galerie-settings").dataset.settings)
  const point = settings[point_id]

  if (!point) return ""

  if (point["pictures"].length < 1) return ""

  const pictures = point["pictures"].map(p => {
    let code = `<div><a href="${p[0]}" target="_blank"><img src="${p[1]}" alt="" data-lightbox /></a>`
    if (!!p[3]) {
      code += `<a href="${p[3]}" target="_blank">${p[2]}</a>`
    } else {
      code += `<a href="${p[0]}" target="_blank">${p[2]}</a>`
    }
    code += "</div>"
    return code
  })

  return `<div class="content-galerie">${pictures.join("")}</div>`
}
