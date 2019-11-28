# Web application API 

All methods, except Login, returns **401** status code, if token wasn’t provided. **200** if success. 

---
### (POST) login/  

 - **user**: { username: string, password: string } 

 - **returns**: token 

   + **401**: credentials are not valid
   + **400**: username or password wasn't provided
---
### (POST) logout/ 

  - **returns**: - 

---
### (GET) core_sample/ 

  - **returns**: array of { csId: string, csName: string, date: date-string, status: string, author: string }. Status could be one of “analysed, inProcess, notAnalysed, error”. Returns only that core samples, which was uploaded by user. 
---
### (GET) core_sample/{csId} 

  - **returns**: if csId is valid, returns { csName: string, date: date-string, status: string, author: string }. **status** could be one of “analysed, inProcess, notAnalysed, error”. 

    + **404**: core sample not found. 
---
### (DELETE) core_sample/{csId}/delete 

  - **csId**: string 

  - **returns**: - 

    + **404**: core sample not found. 

    + **403**: user is not an author of the core sample.
---   
### (GET) core_sample/{csId}/markup 

  - **returns**: { uvImgs, dlImgs, markup: { rock, oil, carbon, distruction} }. 

  - **dlImgs**, **uvImgs**: array of { src: string, height: int, width: int, absHeight: int } 

  - **rock**, **oil**, **carbon**, **distruction**: array of { class: string, absHeight: integer } 

    + **404**: core sample not found. 
---
### (PUT) core_sample/{csId}/markup 

  - **markup**: { rock, oil, carbon, distruction}. (See GET request) 

  - **returns**: - 

    + **404**: core sample not found. 

    + **400**: markup is not valid. 
---
### (POST) core_sample/upload/ 

  - **data**: { archive: file, csName: string}. Archive is a zip-archive with special structure. Must contain description.json with fields “deposit”: integer, “hole”: integer, “fragments”: array of  { “dlImg”: string, “uvImg”: string, “top”: float, “bottom”: float }. Each “dlImg” and “uvImg” are references to .jpg images in the archive. Archive should not containt images, which are not referenced in description.json. 

  - **returns**: { warnings: [string], csId: string } 

    + **400**: structure or content of the archive is not valid. 

    + **409** and **csId**: core sample has already been uploaded. 
---
### (PUT) core_sample/{csId}/analyse 

  - **csId**: string 

  - **returns**: -  

    + **400**: core sample with actual csId has been analysed yet. 

    + **404**: core sample not found. 
---
### (PUT) core_sample/status 

  - **csIds**: array of csId: string 

  - **returns**: [string] - array of core sample statuses. 

    + **404**: core sample not found.
    
---
### (PUT) core_sample/statistics

  - **csIds**: array of csId: string
  
  - **returns**: array of { oil: { high: float, low: float, notDefined: float }, carbon: { ... }, ... } - total propotion of each class of every parameter in core samples. 
  
     + **404**: core sample not found.
