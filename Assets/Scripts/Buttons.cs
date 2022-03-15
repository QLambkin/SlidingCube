using UnityEngine;
using UnityEngine.SceneManagement;

public class Buttons : MonoBehaviour
{
    public void Quit()
    {
        Debug.Log("QUIT");
        Application.Quit();                 //quits application
    }

    public void Menu()
    {
        Debug.Log("Main Menu");
        SceneManager.LoadScene("Menu");     //loads menu scene
    }

    public void StartButton()
    {
        Debug.Log("Start");
        SceneManager.LoadScene("Level");    //loads the level scene
    }

    public void Credits()
    {
        Debug.Log("Credits");
        SceneManager.LoadScene("Credits");  //loads credits scene
    }

    public void ResetScore()
    {
        PlayerPrefs.SetInt("Highscore", 0); //resets the high score to 0
    }
}
