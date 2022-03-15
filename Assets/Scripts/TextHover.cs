using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class TextHover : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    Text txt;                                           //text
    Color baseColor;                                    //standard color of text
    Color hoverColor = new Color(214, 214, 214, 255);    //color of text when cursor is hovering over button

    void Start()
    {
        txt = GetComponentInChildren<Text>();   //get text in Text
        baseColor = txt.color;                  //sets base color to initial text color
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        txt.color = hoverColor;  //sets text color to the hover color
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        txt.color = baseColor;  //sets text color back to base color
    }
}